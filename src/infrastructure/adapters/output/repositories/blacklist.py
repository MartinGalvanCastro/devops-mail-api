from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.domain.entities.blacklists import Blacklist
from src.domain.repositories.blacklist import IBlacklistRepository
from src.infrastructure.adapters.output.db.models import BlacklistModel


class BlacklistRepository(IBlacklistRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Blacklist) -> Blacklist:
        blacklist = BlacklistModel(**data.model_dump())
        self.session.add(blacklist)
        await self.session.commit()
        await self.session.refresh(blacklist)
        return Blacklist.model_validate(blacklist, from_attributes=True)

    async def get_by_email(self, email: str) -> Blacklist | None:
        query = select(BlacklistModel).where(BlacklistModel.email == email)
        result = await self.session.execute(query)
        blacklist = result.scalars().first()
        if blacklist is None:
            return None
        return Blacklist.model_validate(blacklist, from_attributes=True)
