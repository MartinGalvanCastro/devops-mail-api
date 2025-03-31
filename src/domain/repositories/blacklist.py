from src.domain.entities.blacklists import Blacklist


class IBlacklistRepository:
    async def create(self, data: Blacklist) -> Blacklist:
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Blacklist | None:
        raise NotImplementedError
