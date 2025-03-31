from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.adapters.output.db.base import Base
from src.infrastructure.adapters.output.db.mixins import (
    TimestampMixin,
    UUIDIdMixin,
)


class BlacklistModel(Base, UUIDIdMixin, TimestampMixin):
    __tablename__ = "blacklist"
    email: Mapped[str] = mapped_column(String(255))
    app_uuid: Mapped[UUID]
    blocked_reason: Mapped[str] = mapped_column(String(255))
    ip_address: Mapped[str] = mapped_column(String(16))
