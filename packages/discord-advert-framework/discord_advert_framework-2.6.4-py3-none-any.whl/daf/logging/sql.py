"""
    The sql module contains definitions related to the
    relational database logging that is available in this shiller.
    It is only used if the sql logging is enabled by passing
    the daf.run function with the SqlCONTROLLER object.

    .. versionchanged:: v2.1
        Made SQL an optional functionality
"""
from datetime import datetime, date
from typing import Callable, Dict, List, Literal, Any, Union, Optional, Tuple
from contextlib import suppress
from typeguard import typechecked

from .tracing import TraceLEVELS, trace

from . import _logging as logging

import json
import copy
import asyncio

from .. import misc


class GLOBALS:
    """
    Stores global module variables.
    """
    lt_types = []


# ------------------------------------ Configuration -------------------------------
SQL_MAX_SAVE_ATTEMPTS = 5
SQL_RECOVERY_TIME = 1
SQL_RECONNECT_TIME = 5 * 60
SQL_ENABLE_DEBUG = False
SQL_TABLE_CACHE_SIZE = 1000
# Dictionary mapping the database dialect to it's connector
DIALECT_CONN_MAP = {
    "sqlite": "aiosqlite",
    "mssql": "pymssql",
    "postgresql": "asyncpg",
    "mysql": "asyncmy"
}
# ------------------------------------ Optional ------------------------------------
try:
    from sqlalchemy import (
        SmallInteger, Integer, BigInteger, DateTime,
        Sequence, String, JSON, select, text, ForeignKey, func, case
    )
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.engine import URL as SQLURL, create_engine
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import (
        sessionmaker,
        Session,
        DeclarativeBase,
        mapped_column,
        column_property,
        relationship,
        Mapped,
    )
    import sqlalchemy as sqa
    SQL_INSTALLED = True
except ImportError:
    DeclarativeBase = object
    AsyncSession = object
    Session = object
    SQLAlchemyError = Exception
    ORMBase = object
    SQL_INSTALLED = False
# ----------------------------------------------------------------------------------


__all__ = (
    "LoggerSQL",
)


def register_type(lookuptable: Literal["GuildTYPE", "MessageTYPE", "MessageMODE"],
                  name_override: Optional[str] = None) -> Callable:
    """
    Returns a decorator which will create a row inside <lookuptable> table.

    Parameters
    ------------
    lookuptable: Literal["GuildTYPE", "MessageTYPE", "MessageMODE"]
        Name of the lookup table to insert the value into.
    name_override: Optional[str]
        Optional name override for the object to insert into the ``lookuptable``.
        If this is not passed, class name is used.

    Raises
    --------------
    ValueError
        Lookup table not found.
    """
    def decorator_register_type(cls):
        # Iterate thru all module globals to find the lookup table
        if SQL_INSTALLED:
            for table_cls in ORMBase.__subclasses__():
                if table_cls.__tablename__ == lookuptable:
                    GLOBALS.lt_types.append(table_cls(name_override if name_override is not None else cls.__name__))
                    break
            else:
                raise ValueError(f"Lookup table {lookuptable} not found")

        return cls

    if name_override is not None:
        return decorator_register_type(object)

    return decorator_register_type


class ORMBase(DeclarativeBase):
    "Base for all of ORM classes"

    def __eq__(self, value: object) -> bool:
        try:
            return self.id == value.id and type(self) is type(value)
        except AttributeError:
            return super().__eq__(value)

    def __hash__(self):
        try:
            return self.id << 4 | id(type(self)) >> 8
        except AttributeError:
            return super().__hash__()


class TableCache:
    """
    Used for caching table values to IDs for faster access.
    When maximum cache is exceeded, 1/4 of the first added elements is purged
    from cache.

    Parameters
    -------------
    table: ORMBase
        The table this cache is for.
    limit: int
        Max elements to hold.
    """
    def __init__(self, table: ORMBase, limit: int):
        self.table = table
        self.limit = limit
        self.data = {}

    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts value to a specific key

        Parameters
        ------------
        key: Any
            Where to insert.
        value: Any
            What to insert.
        """
        if len(self.data) == self.limit:
            # Remove 1/4 of the cache
            for i in range(int(len(self.data) / 4)):
                self.remove()

        if key in self.data:
            # Remove the value if it already exists
            del self.data[key]

        # Add item to cache
        self.data[key] = value

    def get(self, key: Any) -> Any:
        """
        Returns the cached value.

        Parameters
        key: Any
            The key at which cached value is located.
        """
        return self.data.get(key)

    def remove(self, key: Optional[Any] = None) -> None:
        """
        Removes the cache item at key.

        Parameters
        ------------
        key: Optional[Any]
            The key at which to remove the cached object.
            If not passed, removes first element in cache.

        Raises
        ---------
        ValueError
            The item is not present in the cache.
        ValueError
            No elements are present in cache.
        """
        if key is None:
            if not len(self.data):
                raise ValueError("No elements are present in cache.")

            key = next(iter(self.data))

        del self.data[key]

    def clear(self) -> None:
        "Clears the cache of all values"
        self.data.clear()

    def get_table(self) -> ORMBase:
        "Returns the table this cache is for"
        return self.table

    def exists(self, key: Any) -> bool:
        """
        Returns True if the key is cached.

        Parameters
        -----------
        key: Any
            Cache key to check.
        """
        return key in self.data


@misc.doc_category("Logging reference", path="logging.sql")
class LoggerSQL(logging.LoggerBASE):
    """
    Used for controlling the SQL database used for message logs.

    Parameters
    ------------
    username: Optional[str]
        Username to login to the database with.
    password: Optional[str]
        Password to use when logging into the database.
    server: Optional[str]
        Address of the server.
    port: Optional[int]
        The port of the database server.
    database: Optional[str]
        Name of the database used for logs.
    dialect: Optional[str]
        Dialect or database type (SQLite, mssql, )
    fallback: Optional[LoggerBASE]
        The fallback manager to use in case SQL logging fails.
        (Default: :class:`~daf.logging.LoggerJSON` ("History"))

    Raises
    ----------
    ValueError
        Unsupported dialect (db type).
    """

    @typechecked
    def __init__(self,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 server: Optional[str] = None,
                 port: Optional[int] = None,
                 database: Optional[str] = None,
                 dialect: Literal["sqlite", "mssql", "postgresql", "mysql"] = None,
                 fallback: Optional[logging.LoggerBASE] = ...):

        if not SQL_INSTALLED:
            raise ModuleNotFoundError("Need to install extra requirements: pip install discord-advert-framework[sql]")

        if fallback is Ellipsis:
            # Cannot use None as this can be a legit user value
            # and cannot pass directly due to Sphinx issues
            fallback = logging.LoggerJSON("History")

        if dialect is None:
            dialect = "sqlite"

        dialect = dialect.lower()
        if dialect not in DIALECT_CONN_MAP:
            raise ValueError(f"Unsupported 'dialect': '{dialect}'. Supported: {tuple(DIALECT_CONN_MAP.keys())}.")

        # Save the connection parameters
        self.is_async = False  # Set in _begin_engine
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.database = database if database is not None else "messages"
        self.dialect = dialect

        if self.dialect == "sqlite":
            self.database += ".db"

        # Set in ._begin_engine
        self.engine: sqa.engine.Engine = None
        self.session_maker: sessionmaker = None

        # Semaphore used to prevent multiple tasks from trying to access the `._save_log()` method at once.
        # Also used in the `.update()` method to prevent race conditions.
        self.safe_sem = asyncio.Semaphore(1)
        self.reconnecting = False  # Flag that is True while reconnecting, used for emergency exit of other tasks

        # Caching (to avoid unnecessary queries)
        # Lookup table caching
        self.message_mode_cache = TableCache(MessageMODE, SQL_TABLE_CACHE_SIZE)
        self.message_type_cache = TableCache(MessageTYPE, SQL_TABLE_CACHE_SIZE)
        self.guild_type_cache = TableCache(GuildTYPE, SQL_TABLE_CACHE_SIZE)

        # Other object caching
        self.guild_user_cache = TableCache(GuildUSER, SQL_TABLE_CACHE_SIZE)
        self.channel_cache = TableCache(CHANNEL, SQL_TABLE_CACHE_SIZE)
        self.data_history_cache = TableCache(DataHISTORY, SQL_TABLE_CACHE_SIZE)

        super().__init__(fallback)

    async def _run_async(self, method: Callable, *args, **kwargs):
        """
        Helper method that abstracts calls of
        non async functions so await can always be used

        Parameters
        -----------
        method: Callable
            The async/non-async method to call
        args
            Positional arguments for the method
        kwargs
            Keyword arguments for the method
        """
        raise NotImplementedError  # This function is defined in .begin_engine

    def _add_to_cache(self, table: ORMBase, key: Any, value: Any) -> None:
        """
        Adds a value to the internal cache of a certain table.

        Parameters
        ------------
        table: Base
            Name of the table to cache the row in.
        key: Any
            Row key.
        value: Any
            Row value.
        """
        for var in vars(self).values():
            if isinstance(var, TableCache) and table is var.get_table():
                var.insert(key, value)

    def _clear_caches(self, *to_clear: str) -> None:
        """
        Clears the caching dictionaries inside the object that match any of the tables.

        Parameters
        -----------
        *to_clear: str
            Custom number of positional arguments of caching dictionaries to clear.
        """
        if len(to_clear) == 0:  # Clear all cached tables if nothing was passed
            to_clear = [cache for cache in vars(self).values() if isinstance(cache, TableCache)]
        else:
            to_clear = [getattr(self, table) for table in to_clear if hasattr(self, table)]

        for k in to_clear:
            k.clear()

    async def _reconnect_after(self, wait: int) -> None:
        """
        Reconnects the SQL manager to the database after <wait> if it was disconnected.

        Parameters
        -----------
        wait: int
            Time in seconds after which reconnect.
        """
        async def _reconnector():
            session: Union[Session, AsyncSession]
            # Always try to reconnect
            while True:
                trace(f"Retrying to connect in {wait} seconds.")
                await asyncio.sleep(wait)
                trace(f"Reconnecting to database {self.database}.")
                with suppress(SQLAlchemyError, ConnectionError):
                    async with self.session_maker() as session:
                        await self._run_async(session.execute, select(text("1")))  # Test with SELECT 1;

                    trace(f"Reconnected to the database {self.database}.")
                    self.reconnecting = False
                    logging._set_logger(self)
                    return

        self.reconnecting = True
        logging._set_logger(self.fallback)
        asyncio.create_task(_reconnector())

    async def _generate_lookup_values(self) -> None:
        """
        Generates the lookup values for all the different classes the @register_type decorator was used on.

        Raises
        -------------
        RuntimeError
            Raised when lookuptable values could not be inserted into the database.
        """
        try:
            trace("Generating lookuptable values...", TraceLEVELS.NORMAL)
            async with self.session_maker() as session:
                # Deep copied to prevent SQLAlchemy from deleting the data
                for to_add in copy.deepcopy(GLOBALS.lt_types):
                    existing = await self._run_async(
                        session.execute,
                        select(type(to_add)).where(type(to_add).name == to_add.name)
                    )
                    existing = existing.fetchone()
                    if existing is not None:
                        existing = existing[0]
                    else:
                        session.add(to_add)
                        await self._run_async(session.commit)
                        existing = to_add

                    self._add_to_cache(type(to_add), to_add.name, existing)
        except Exception as ex:
            raise RuntimeError("Unable to create lookuptables' rows.") from ex

    async def _create_tables(self) -> None:
        """
        Creates tables from the SQLAlchemy's descriptor classes

        Raises
        -----------
        RuntimeError
            Raised when tables could not be created.
        """
        try:
            trace("Creating tables...", TraceLEVELS.NORMAL)
            if self.is_async:
                async with self.engine.begin() as tran:
                    await tran.run_sync(ORMBase.metadata.create_all)
            else:
                with self.engine.connect() as tran:
                    tran.run_callable(ORMBase.metadata.create_all)

        except Exception as ex:
            raise RuntimeError("Unable to create all the tables.") from ex

    def _begin_engine(self) -> None:
        """
        Creates the sqlalchemy engine.

        Raises
        ----------------
        RuntimeError
            Raised when the engine could not connect to the specified database.
        """
        try:
            dialect = self.dialect
            if dialect == "mssql":
                # The only dialect that doesn't have async connectors
                async def _run_async(method: Callable, *args, **kwargs):
                    return method(*args, **kwargs)

                self.is_async = False
                create_engine_ = create_engine
                session_class = Session
            else:
                async def _run_async(method: Callable, *args, **kwargs):
                    return await method(*args, **kwargs)

                self.is_async = True
                create_engine_ = create_async_engine
                session_class = AsyncSession

            sqlurl = SQLURL.create(
                f"{dialect}+{DIALECT_CONN_MAP[dialect]}",
                self.username,
                self.password,
                self.server,
                self.port,
                self.database
            )

            self.engine = create_engine_(sqlurl, echo=SQL_ENABLE_DEBUG)
            self._run_async = _run_async

            class SessionWrapper(session_class):
                """
                Wrapper class for the session that can always be used
                in async mode, even if the session it wraps is not async.
                """
                if self.is_async:
                    async def __aenter__(self_):
                        return await super().__aenter__()

                    async def __aexit__(self_, *args):
                        return await super().__aexit__(*args)
                else:
                    async def __aenter__(self_):
                        return self_.__enter__()

                    async def __aexit__(self_, *args):
                        return self_.__exit__(*args)

            self.session_maker = sessionmaker(bind=self.engine, class_=SessionWrapper, expire_on_commit=False)
        except Exception as ex:
            raise RuntimeError(f"Unable to start engine.\nError: {ex}")

    async def initialize(self) -> None:
        """
        This method initializes the connection to the database, creates the missing tables
        and fills the lookup tables with types defined by the register_type(lookup_table) function.

        .. note::
            This is automatically called when running the daf.

        Raises
        -----------
        Any
            from ``._begin_engine()``
            from ``._create_tables()``
            from ``._generate_lookup_values()``
        """
        # Create engine for communicating with the SQL base
        self._begin_engine()
        # Create tables and the session class bound to the engine
        await self._create_tables()
        # Insert the lookuptable values
        await self._generate_lookup_values()
        await super().initialize()

    async def _get_insert_guild(self,
                                snowflake: int,
                                name: str,
                                guild_type: int,
                                session: Union[AsyncSession, Session]) -> int:
        """
        Inserts the guild into the db if it doesn't exist,
        adds it to cache and returns it's internal db id from cache.

        Parameters
        ------------
        snowflake: int
            The snowflake of the guild.
        name: name
            The name of the guild.
        guild_type: int
            ID of key pointing to guild_type.
        session: Union[AsyncSession, Session]
            The session to use as transaction.
        """
        result = None
        if not self.guild_user_cache.exists(snowflake):
            result = await self._run_async(
                session.execute,
                select(GuildUSER).where(GuildUSER.snowflake_id == snowflake)
            )
            result = result.first()
            if result is not None:
                result = result[0]
            else:
                result = GuildUSER(guild_type, snowflake, name)
                savepoint = await self._run_async(session.begin_nested)  # Savepoint
                session.add(result)
                await self._run_async(savepoint.commit)
                result = result

            self.guild_user_cache.insert(snowflake, result)
        else:
            result = self.guild_user_cache.get(snowflake)

        return result

    async def _get_insert_channels(self,
                                   channels: List[dict],
                                   guild: "GuildUSER",
                                   session: Union[AsyncSession, Session]) -> List[Dict[int, Union[str, None]]]:
        """
        Adds missing channels to the database, then caches those added
        for performance.

        Parameters
        ------------
        channels: List[dict]
            List of dictionaries containing values for snowflake id ("id") and name of the channel ("name").
            If sending to failed, it also contains text like description of the error ("reason").
        guild: GuildUSER
            The internal DB id of the guild where the channels are in.
        session: Union[AsyncSession, Session]
            Session to use for transaction.

        Return
        -------------
        List[Dict[int, Union[str, None]]]
            List of dictionaries containing database ID of a channel and a reason why sending to channel failed.
        """

        # Put into cache if it is not already
        # Get snowflakes that are not cached
        not_cached = [{"id": x["id"], "name": x["name"]} for x in channels if not self.channel_cache.exists(x["id"])]
        not_cached_snow = [x["id"] for x in not_cached]
        if len(not_cached):
            # Search the database for non cached channels
            result = await self._run_async(
                session.execute,
                select(CHANNEL).where(CHANNEL.snowflake_id.in_(not_cached_snow))
            )
            result = result.all()
            for (channel,) in result:
                self.channel_cache.insert(channel.snowflake_id, channel)

            # Add the channels that are not in the database
            to_add = [
                CHANNEL(x["id"], x["name"], guild)
                for x in not_cached if not self.channel_cache.exists(x["id"])
            ]
            if len(to_add):
                savepoint = await self._run_async(session.begin_nested)  # Savepoint
                session.add_all(to_add)
                await self._run_async(savepoint.commit)
                for channel in to_add:
                    self.channel_cache.insert(channel.snowflake_id, channel)

        # Get from cache
        ret = [(self.channel_cache.get(d["id"]), d.get("reason", None)) for d in channels]
        return ret

    async def _get_insert_data(self, data: dict, session: Union[AsyncSession, Session]) -> int:
        """
        Get's data's row ID from the cache/database, if it does not exists,
        it inserts into the database and then caches the value.

        Parameters
        -------------
        data: dict
            The data dictionary which represents sent data
        session: Union[AsyncSession, Session]
            Session to use for transaction.

        Returns
        -------------
        int
            Primary key of a row inside DataHISTORY table.
        """
        result: tuple = None
        const_data = json.dumps(data)

        if not self.data_history_cache.exists(const_data):
            result = await self._run_async(
                session.execute,
                select(DataHISTORY).where(DataHISTORY.content.cast(String) == const_data)
            )
            result = result.first()
            if result is None:
                # Add to the database
                to_add = DataHISTORY(const_data)
                savepoint = await self._run_async(session.begin_nested)
                session.add(to_add)
                await self._run_async(savepoint.commit)
                result = (to_add,)

            self.data_history_cache.insert(const_data, result[0])

        return self.data_history_cache.get(const_data)

    async def _stop_engine(self):
        """
        Closes the engine and the cursor.
        """
        await self._run_async(self.engine.dispose)

    async def _handle_error(self,
                            exc: SQLAlchemyError) -> bool:
        """
        Used to handle errors that happen in the _save_log method.

        Parameters
        ---------------
        exc: SQLAlchemyError
            The exception object.

        Return
        --------
        bool
            Returns True on successful handling.
        """
        res = True
        await asyncio.sleep(SQL_RECOVERY_TIME)
        try:
            if exc.connection_invalidated:
                res = False
                await self._reconnect_after(SQL_RECONNECT_TIME)
            else:
                await self._create_tables()
                self._clear_caches()
                await self._generate_lookup_values()

        except Exception:
            # Error could not be handled, stop the engine
            res = False
            await self._stop_engine()

        return res  # Returns if the error was handled or not

    # _async_safe prevents multiple tasks from attempting to do operations on the database at the same time.
    # This is to avoid eg. procedures being called while they are being created,
    # handle error being called from different tasks, update method from causing a race condition,etc
    @misc._async_safe("safe_sem", 1)
    async def _save_log(self,
                        guild_context: dict,
                        message_context: dict,
                        author_context: dict):
        """
        This method saves the log generated by the xGUILD object into the database.

        Parameters
        -------------
        guild_context: dict
            Context generated by the xGUILD object, see guild.xGUILD.generate_log_context() for more info.
        message_context: dict
            Context generated by the xMESSAGE object, see guild.xMESSAGE.generate_log_context() for more info.
        author_context: dict
            Context generated by the ACCOUNT object, see ACCOUNT.generate_log_context() for more info.

        Raises
        --------
        RuntimeError
            Saving failed within n times or error recovery failed.
        """

        if self.reconnecting:
            # The SQL logger is in the middle of reconnection process
            # This means the logging is switched to something else but we still got here
            # since we entered before that happened and landed on a semaphore.
            await logging.save_log(guild_context, message_context)
            return

        # Parse the data
        author_name: str = author_context.get("name")
        author_snowflake: str = author_context.get("id")
        sent_data: dict = message_context.get("sent_data")
        guild_snowflake: int = guild_context.get("id")
        guild_name: str = guild_context.get("name")
        channels: List[dict] = message_context.get("channels", None)
        dm_success_info: dict = message_context.get("success_info", None)
        dm_success_info_reason: str = None
        message_mode: Union[int, str, None] = message_context.get("mode", None)

        if dm_success_info is not None:
            if "reason" in dm_success_info:
                dm_success_info_reason = dm_success_info["reason"]

        _channels = []
        if channels is not None:
            channels = channels['successful'] + channels['failed']

        session: Union[AsyncSession, Session]
        for tries in range(SQL_MAX_SAVE_ATTEMPTS):
            try:
                # Lookup table values
                guild_type_obj = self.guild_type_cache.get(guild_context["type"])
                message_type_obj = self.message_type_cache.get(message_context["type"])
                message_mode_obj = self.message_mode_cache.get(message_mode)
                # Insert guild into the database and cache if it doesn't exist
                async with self.session_maker() as session:
                    guild_obj = await self._get_insert_guild(guild_snowflake, guild_name, guild_type_obj, session)
                    if channels is not None:
                        # Insert channels into the database and cache if it doesn't exist
                        _channels = await self._get_insert_channels(channels, guild_obj, session)

                    data_obj = await self._get_insert_data(sent_data, session)
                    author_obj = await self._get_insert_guild(
                        author_snowflake,
                        author_name,
                        self.guild_type_cache.get("USER"),
                        session
                    )

                    # Save message log
                    message_log_obj = MessageLOG(
                        data_obj,
                        message_type_obj,
                        message_mode_obj,
                        dm_success_info_reason,
                        guild_obj,
                        author_obj,
                        [
                            MessageChannelLOG(channel, reason)
                            for channel, reason in _channels
                        ],
                    )
                    session.add(message_log_obj)
                    await self._run_async(session.commit)

                break
            except SQLAlchemyError as exc:
                # Run in executor to prevent blocking
                if not await self._handle_error(exc):
                    raise RuntimeError("Unable to handle SQL error") from exc

        else:
            raise RuntimeError(f"Unable to save log within {SQL_MAX_SAVE_ATTEMPTS} tries")

    async def _get_guild(self, id_: int, session: Union[AsyncSession, Session]):
        guilduser: GuildUSER = self.guild_user_cache.get(id_)
        if guilduser is not None:
            return guilduser

        try:
            _ret = (await self._run_async(
                session.execute,
                select(GuildUSER)
                .where(GuildUSER.snowflake_id == id_))
            ).first()
            return _ret[0] if _ret is not None else None
        except SQLAlchemyError:
            return None

    async def analytic_get_num_messages(
            self,
            guild: Union[int, None] = None,
            author: Union[int, None] = None,
            after: Union[datetime, None] = None,
            before: Union[datetime, None] = None,
            guild_type: Union[Literal["USER", "GUILD"], None] = None,
            message_type: Union[Literal["TextMESSAGE", "VoiceMESSAGE", "DirectMESSAGE"], None] = None,
            sort_by: Literal["successful", "failed", "guild_snow", "guild_name", "author_snow", "author_name"] = "successful",
            sort_by_direction: Literal["asc", "desc"] = "desc",
            limit: int = 500,
            group_by: Literal["year", "month", "day"] = "day"
    ) -> List[Tuple[date, int, int, int, str, int, str]]:
        """

        Parameters
        -----------
        guild: int
            The snowflake id of the guild.
        author: int
            The snowflake id of the author.
        after: Union[datetime, None] = None
            Only count messages sent after the datetime.
        before: Union[datetime, None]
            Only count messages sent before the datetime.
        guild_type: Literal["USER", "GUILD"] | None,
            Type of guild.
        message_type: Literal["TextMESSAGE", "VoiceMESSAGE", "DirectMESSAGE"] | None,
            Type of message.
        sort_by: Literal["successful", "failed", "guild_snow", "guild_name", "author_snow", "author_name"],
            Sort items by selected.
            Defaults to "successful"
        sort_by_direction: Literal["asc", "desc"]
            Sort items by ``sort_by`` in selected direction (asc = ascending, desc = descending).
            Defaults to "desc"
        limit: int = 500
            Limit of the rows to return. Defaults to 500.
        group_by: Literal["year", "month", "day"]
            Results returned are grouped by ``group_by``

        Returns
        --------
        list[tuple[date, int, int, int, str, int, str]]
            List of tuples.

            Each tuple contains:

            - Date
            - Successfule sends
            - Failed sends
            - Guild snowflake id,
            - Guild name
            - Author snowflake id,
            - Author name

        Raises
        ------------
        SQLAlchemyError
            There was a problem with the database.
        """
        if after is None:
            after = datetime.min

        if before is None:
            before = datetime.max

        regions = ["day", "month", "year"]
        regions = reversed(regions[regions.index(group_by):])
        extract_stms = []
        for region_ in regions:
            extract_stms.append(func.extract(region_, MessageLOG.timestamp).cast(Integer))

        async with self.session_maker() as session:
            conditions = []
            if guild is not None:
                conditions.append(
                    MessageLOG.guild.has(GuildUSER.snowflake_id == guild)
                )

            if author is not None:
                conditions.append(
                    MessageLOG.author.has(GuildUSER.snowflake_id == author)
                )

            if guild_type is not None:
                conditions.append(
                    MessageLOG.guild.has(
                        GuildUSER.guild_type.has(GuildTYPE.name == guild_type)
                    )
                )

            if message_type is not None:
                conditions.append(
                    MessageLOG.message_type.has(MessageTYPE.name == message_type)
                )

            count = (await self._run_async(
                session.execute,
                select(
                    *extract_stms,
                    func.sum(case((MessageLOG.success_rate > 0, 1), else_=0)).label("successful"),
                    func.sum(case((MessageLOG.success_rate == 0, 1), else_=0)).label("failed"),
                    select(GuildUSER.snowflake_id).where(GuildUSER.id == MessageLOG.guild_id).scalar_subquery().label("guild_snow"),
                    select(GuildUSER.name).where(GuildUSER.id == MessageLOG.guild_id).scalar_subquery().label("guild_name"),
                    select(GuildUSER.snowflake_id).where(GuildUSER.id == MessageLOG.author_id).scalar_subquery().label("author_snow"),
                    select(GuildUSER.name).where(GuildUSER.id == MessageLOG.author_id).scalar_subquery().label("author_name")
                )
                .where(
                    MessageLOG.timestamp.between(after, before),
                    *conditions
                )
                .group_by(*extract_stms, MessageLOG.guild_id, MessageLOG.author_id)
                .limit(limit)
                .order_by(text(f"{sort_by} {sort_by_direction}"))
            )).all()

            extract_stm_len = len(extract_stms)
            count = [
                (date(*s[:extract_stm_len], *([1] * (3 - extract_stm_len))), *s[extract_stm_len:])
                for s in count
            ]

            return count

    async def analytic_get_message_log(
            self,
            guild: Union[int, None] = None,
            author: Union[int, None] = None,
            after: Union[datetime, None] = None,
            before: Union[datetime, None] = None,
            success_rate: Tuple[float, float] = (0, 100),
            guild_type: Union[Literal["USER", "GUILD"], None] = None,
            message_type: Union[Literal["TextMESSAGE", "VoiceMESSAGE", "DirectMESSAGE"], None] = None,
            sort_by: Literal["timestamp", "success_rate"] = "timestamp",
            sort_by_direction: Literal["asc", "desc"] = "desc",
            limit: int = 500,
    ) -> List["MessageLOG"]:
        """
        Returns a list MessageLOG objects (message logs) that match the parameters.

        Parameters
        --------------
        guild: Union[int, None]
            The snowflake id of the guild.
        author: Union[int, None]
            The snowflake id of the author.
        after: Union[datetime, None]
            Include only messages sent after this datetime.
        before: Union[datetime, None]
            Include only messages sent before this datetime.
        success_rate: tuple[int, int]
            Success rate tuple containing minimum success rate and maximum success
            rate the message log can have for it to be included.
            Success rate is meassured in % and it is defined by:

            Successuly sent channels / all channels.
        guild_type: Literal["USER", "GUILD"] | None,
            Type of guild.
        message_type: Literal["TextMESSAGE", "VoiceMESSAGE", "DirectMESSAGE"] | None,
            Type of message.
        sort_by: Literal["timestamp", "success_rate", "data"],
            Sort items by selected.
            Defaults to "timestamp"
        sort_by_direction: Literal["asc", "desc"] = "desc"
            Sort items by ``sort_by`` in selected direction (asc = ascending, desc = descending).
            Defaults to "desc"
        limit: int = 500
            Limit of the message logs to return. Defaults to 500.

        Return
        ---------
        list[MessageLOG]
            List of the message logs.
        """
        if after is None:
            after = datetime.min

        if before is None:
            before = datetime.max

        # Obtain internal guild id

        async with self.session_maker() as session:
            conditions = []
            if guild is not None:
                conditions.append(
                    MessageLOG.guild.has(GuildUSER.snowflake_id == guild)
                )

            if author is not None:
                conditions.append(
                    MessageLOG.author.has(GuildUSER.snowflake_id == author)
                )

            if guild_type is not None:
                conditions.append(
                    MessageLOG.guild.has(
                        GuildUSER.guild_type.has(GuildTYPE.name == guild_type)
                    )
                )

            if message_type is not None:
                conditions.append(
                    MessageLOG.message_type.has(MessageTYPE.name == message_type)
                )

            messages = await self._run_async(
                session.execute,
                select(MessageLOG)
                .where(
                    MessageLOG.success_rate.between(*success_rate),
                    MessageLOG.timestamp.between(after, before),
                    *conditions
                ).order_by(getattr(getattr(MessageLOG, sort_by), sort_by_direction)()).limit(limit)
            )

            return list(*zip(*messages.unique().all()))

    @misc._async_safe("safe_sem", 1)
    async def update(self, **kwargs):
        """
        .. versionadded:: v2.0

        Used for changing the initialization parameters the object was initialized with.

        .. warning::
            Upon updating, the internal state of objects get's reset,
            meaning you basically have a brand new created object.
            It also resets the message objects.

        Parameters
        -------------
        **kwargs: Any
            Custom number of keyword parameters which you want to update,
            these can be anything that is available during the object creation.

        Raises
        -----------
        TypeError
            Invalid keyword argument was passed.
        Other
            Raised from .initialize() method.
        """
        try:
            await self._stop_engine()
            await misc._update(self, **kwargs)
        except Exception:
            # Reinitialize since engine was disconnected
            await self.initialize()
            raise


if SQL_INSTALLED:
    # Do not create ORM classes if the optional group is not installed
    class MessageTYPE(ORMBase):
        """
        Lookup table for storing xMESSAGE types

        Parameters
        -----------
        name: str
            Name of the xMESSAGE class.
        """
        __tablename__ = "MessageTYPE"

        id = mapped_column(
            SmallInteger().with_variant(Integer, "sqlite"),
            Sequence("msg_tp_seq", 0, 1, minvalue=0, maxvalue=32767, cycle=True),
            primary_key=True
        )
        name = mapped_column(String(3072), unique=True)

        def __init__(self, name: str = None):
            self.name = name

    class MessageMODE(ORMBase):
        """
        Lookup table for storing message sending modes.

        Parameters
        -----------
        name: str
            Name of the xMESSAGE class.
        """

        __tablename__ = "MessageMODE"

        id = mapped_column(
            SmallInteger().with_variant(Integer, "sqlite"),
            Sequence("msg_mode_seq", 0, 1, minvalue=0, maxvalue=32767, cycle=True),
            primary_key=True
        )
        name = mapped_column(String(3072), unique=True)

        def __init__(self, name: str = None):
            self.name = name

    class GuildTYPE(ORMBase):
        """
        Lookup table for storing xGUILD types

        Parameters
        -----------
        name: str
            Name of the xMESSAGE class.
        """

        __tablename__ = "GuildTYPE"

        id: Mapped[int] = mapped_column(
            SmallInteger().with_variant(Integer, "sqlite"),
            Sequence("guild_tp_seq", 0, 1, minvalue=0, maxvalue=32767, cycle=True),
            primary_key=True
        )
        name = mapped_column(String(3072), unique=True)

        def __init__(self, name: str = None):
            self.name = name

    class GuildUSER(ORMBase):
        """
        Table for storing different guilds and users.

        Parameters
        -----------
        guild_type: int
            Foreign key pointing to GuildTYPE.id.
        snowflake: int
            Discord's snowflake ID of the guild.
        name: str
            The name of the guild.
        """
        __tablename__ = "GuildUSER"

        id = mapped_column(
            Integer,
            Sequence("guild_user_seq", 0, 1, minvalue=0, maxvalue=2147483647, cycle=True),
            primary_key=True
        )
        snowflake_id = mapped_column(BigInteger, index=True)
        name = mapped_column(String(3072))
        guild_type_id: Mapped[int] = mapped_column(ForeignKey("GuildTYPE.id"))
        guild_type: Mapped["GuildTYPE"] = relationship(lazy="joined")

        def __init__(self,
                     guild_type: GuildTYPE,
                     snowflake: int,
                     name: str):
            self.snowflake_id = snowflake
            self.name = name
            self.guild_type = guild_type

    class CHANNEL(ORMBase):
        """
        Table for storing different channels.

        Parameters
        -----------
        snowflake: int
            Discord's snowflake ID of the channel.
        name: str
            The name of the channel.
        guild_id: int
            Foreign key pointing to GuildUSER.id.
        """
        __tablename__ = "CHANNEL"
        id = mapped_column(
            Integer,
            Sequence("channel_seq", 0, 1, minvalue=0, maxvalue=2147483647, cycle=True),
            primary_key=True
        )
        snowflake_id = mapped_column(BigInteger)
        name = mapped_column(String(3072))
        guild_id: Mapped[int] = mapped_column(ForeignKey("GuildUSER.id"))
        guild: Mapped["GuildUSER"] = relationship(lazy="joined")

        def __init__(self,
                     snowflake: int,
                     name: str,
                     guild: GuildUSER):
            self.snowflake_id = snowflake
            self.name = name
            self.guild = guild

    class DataHISTORY(ORMBase):
        """
        Table used for storing all the different data(JSON) that was ever sent (to reduce redundancy
        and file size in the MessageLOG).

        Parameters
        -----------
        content: str
            The JSON string representing sent data.
        """
        __tablename__ = "DataHISTORY"

        id = mapped_column(
            Integer,
            Sequence("dhist_seq", 0, 1, minvalue=0, maxvalue=2147483647, cycle=True),
            primary_key=True
        )

        content = mapped_column(JSON())

        def __init__(self,
                     content: dict):
            self.content = content

    class MessageChannelLOG(ORMBase):
        """
        This is a table that contains a log of channels that are linked to a certain message log.

        Parameters
        ------------
        message_log: MessageLOG
            Foreign key pointing to MessageLOG.id.
        channel: CHANNEL
            Foreign key pointing to CHANNEL.id.
        reason: str
            Stringified description of Exception that caused the send attempt to be successful for a certain channel.
        """

        __tablename__ = "MessageChannelLOG"

        log_id: Mapped[int] = mapped_column(Integer, ForeignKey("MessageLOG.id"), primary_key=True)
        channel_id: Mapped[int] = mapped_column(Integer, ForeignKey("CHANNEL.id"), primary_key=True)
        reason = mapped_column(String(3072))

        log: Mapped["MessageLOG"] = relationship(back_populates="channels", uselist=False, lazy="joined")
        channel: Mapped["CHANNEL"] = relationship(lazy="joined")

        def __init__(self,
                     channel: CHANNEL,
                     reason: str = None):
            self.channel = channel
            self.reason = reason

    class MessageLOG(ORMBase):
        """
        Table containing information for each message send attempt.

        NOTE: This table is missing successful and failed channels (or DM success status).
        That is because those are a separate table.

        Parameters
        ------------
        sent_data: DataHISTORY
            DataHISTORY object containing JSON data.
        message_type: MessageTYPE
            MessageTYPE object representing type of the message.
        message_mode: MessageMODE | None
            MessageMODE object representing mode of the message. (TextMESSAGE and DirectMESSAGE only)
        dm_reason: str | None
            The reason why sending to the USER failed. (DirectMESSAGE only)
        guild: GuildUSER
            The guild / user message was sent to.
        author: GuildUSER
            The author of the message.
        channels: List["MessageChannelLOG"]
            List of MessageChannelLOG representing channel the message was sent into and the fail reason.
        """

        __tablename__ = "MessageLOG"

        id = mapped_column(
            Integer,
            Sequence("ml_seq", 0, 1, minvalue=0, maxvalue=2147483647, cycle=True),
            primary_key=True
        )
        sent_data_id: Mapped[int] = mapped_column(ForeignKey("DataHISTORY.id"))
        message_type_id: Mapped[int] = mapped_column(ForeignKey("MessageTYPE.id"))
        guild_id: Mapped[int] = mapped_column(ForeignKey("GuildUSER.id"))
        author_id: Mapped[int] = mapped_column(ForeignKey("GuildUSER.id"))
        # [TextMESSAGE, DirectMESSAGE]
        message_mode_id: Mapped[int] = mapped_column(ForeignKey("MessageMODE.id"), nullable=True)
        dm_reason = mapped_column(String(3072))  # [DirectMESSAGE]
        timestamp = mapped_column(DateTime)

        sent_data: Mapped["DataHISTORY"] = relationship(lazy="joined")
        message_type: Mapped["MessageTYPE"] = relationship(lazy="joined")
        guild: Mapped["GuildUSER"] = relationship(foreign_keys=[guild_id], lazy="joined")
        author: Mapped["GuildUSER"] = relationship(foreign_keys=[author_id], lazy="joined")
        message_mode: Mapped["MessageMODE"] = relationship(lazy="joined")
        channels: Mapped[List["MessageChannelLOG"]] = relationship(back_populates="log", lazy="joined")
        success_rate = column_property(
            case(
                (
                    select(1).where(MessageChannelLOG.log_id == id).limit(1).exists(),
                    100 * select(func.count()).where(MessageChannelLOG.reason.is_(None), MessageChannelLOG.log_id == id)
                    .select_from(MessageChannelLOG)
                    .scalar_subquery() /
                    select(func.count()).where(MessageChannelLOG.log_id == id).select_from(MessageChannelLOG)
                    .scalar_subquery(),
                ),
                else_=case((dm_reason.is_(None), 100), else_=0)
            )
        )

        def __init__(self,
                     sent_data: DataHISTORY = None,
                     message_type: MessageTYPE = None,
                     message_mode: MessageMODE = None,
                     dm_reason: str = None,
                     guild: GuildUSER = None,
                     author: GuildUSER = None,
                     channels: List["MessageChannelLOG"] = None):
            self.sent_data = sent_data
            self.message_type = message_type
            self.message_mode = message_mode
            self.dm_reason = dm_reason
            self.guild = guild
            self.author = author
            self.timestamp = datetime.now()
            self.channels = channels
