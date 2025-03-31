from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.adapters.output.repositories.blacklist import (
    BlacklistRepository,
)


def get_blacklist_repository(session: AsyncSession) -> BlacklistRepository:
    return BlacklistRepository(session)
