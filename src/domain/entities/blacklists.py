from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Blacklist(BaseModel):
    id: UUID | None = None
    email: str = Field(..., max_length=255)
    app_uuid: UUID
    blocked_reason: str = Field(..., max_length=255)
    ip_address: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateBlacklistResponse(BaseModel):
    message: str


class CreateBlacklistRequest(BaseModel):
    email: str
    app_uuid: UUID
    blocked_reason: str


class ValidateEmailInBlacklistResponse(BaseModel):
    is_blacklisted: bool
    blocked_reason: str
