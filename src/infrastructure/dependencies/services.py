from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.blacklist import BlacklistService
from src.infrastructure.dependencies.repositories import get_blacklist_repository


def get_blacklist_service(session: AsyncSession) -> BlacklistService:
    blacklist_repository = get_blacklist_repository(session)
    return BlacklistService(blacklist_repository=blacklist_repository)
