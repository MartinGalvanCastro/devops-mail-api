from src.domain.entities.blacklists import Blacklist, CreateBlacklistRequest
from src.domain.repositories.blacklist import IBlacklistRepository


class BlacklistService:
    def __init__(self, blacklist_repository: IBlacklistRepository):
        self.blacklist_repository = blacklist_repository

    async def create_blacklist(
        self, data: CreateBlacklistRequest, ip_address: str | None = None
    ) -> Blacklist:
        blacklist = Blacklist(
            email=data.email.lower(),
            app_uuid=data.app_uuid,
            blocked_reason=data.blocked_reason,
            ip_address=ip_address,
        )
        created_blacklist = await self.blacklist_repository.create(data=blacklist)
        return created_blacklist

    async def get_blacklist_by_email(self, email: str) -> Blacklist:
        blacklist = await self.blacklist_repository.get_by_email(email=email.lower())
        return blacklist
