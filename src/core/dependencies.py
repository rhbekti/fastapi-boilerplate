from typing import Annotated, AsyncGenerator, Any

from fastapi import Depends
from psycopg_pool import AsyncConnectionPool
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from src.core.config import config

PGPOOL: AsyncConnectionPool | None = None
ENGINE: AsyncEngine | None = None
SESSION_LOCAL: async_sessionmaker[AsyncSession] | None = None


async def init_db_engine() -> None:
    """call on app startup"""
    global PGPOOL, ENGINE, SESSION_LOCAL

    PGPOOL = AsyncConnectionPool(
        conninfo=config.db_url,
        open=False,
        min_size=config.db_pool_min_size,
        max_size=config.db_pool_max_size,
    )

    await PGPOOL.open()

    ENGINE = create_async_engine(
        url="postgresql+psycopg://",
        poolclass=NullPool,
        async_creator=PGPOOL.getconn,
    )

    SESSION_LOCAL = async_sessionmaker(
        bind=ENGINE,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )


async def close_db_engine() -> None:
    """call on app shutdown"""
    global PGPOOL, ENGINE, SESSION_LOCAL

    if ENGINE is not None:
        await ENGINE.dispose()
        ENGINE = None

    if PGPOOL is not None:
        await PGPOOL.close()
        PGPOOL = None

    SESSION_LOCAL = None


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    """ "Create session connection."""
    if SESSION_LOCAL is None:
        raise RuntimeError(
            "DB ENGINE belum diinisialisasi. Pastikan init_db_engine() dipanggil di lifespan."
        )

    async with SESSION_LOCAL() as session:
        try:
            yield session
        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
