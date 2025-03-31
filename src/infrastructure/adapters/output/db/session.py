import logging

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.commons.settings.base import settings

logger = logging.getLogger(__name__)

logger.info(f"Connecting to database at {settings.DB_URL}")

async_engine: AsyncEngine = create_async_engine(
    settings.DB_URL, echo=settings.DEBUG, future=True, pool_pre_ping=True
)

AsyncSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

sync_engine: Engine = create_engine(settings.DB_URL, echo=settings.DEBUG)

SyncSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    expire_on_commit=False,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        try:
            logger.info("Creating a new session..")
            yield session
        finally:
            logger.info("Closing the session..")
            await session.close()


def get_sync_session():
    with SyncSessionLocal() as session:
        try:
            logger.info("Creating a new session..")
            yield session
        finally:
            logger.info("Closing the session..")
            session.close()
