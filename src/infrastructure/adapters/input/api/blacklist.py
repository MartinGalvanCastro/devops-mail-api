import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.blacklists import (
    CreateBlacklistRequest,
    CreateBlacklistResponse,
    ValidateEmailInBlacklistResponse,
)
from src.infrastructure.adapters.output.db.session import get_async_session
from src.infrastructure.dependencies.services import get_blacklist_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/blacklists", response_model=CreateBlacklistResponse)
async def create_blacklist(
    request: Request,
    data: CreateBlacklistRequest,
    session: AsyncSession = Depends(get_async_session),
):
    service = get_blacklist_service(session=session)
    await service.create_blacklist(data=data, ip_address=request.state.client_ip)
    return CreateBlacklistResponse(message="Blacklist created successfully")


@router.get("/blacklists/{email}", response_model=ValidateEmailInBlacklistResponse)
async def validate_email_in_blacklist(
    email: str, session: AsyncSession = Depends(get_async_session)
):
    service = get_blacklist_service(session=session)
    blacklisted_email = await service.get_blacklist_by_email(email=email)
    return ValidateEmailInBlacklistResponse(
        is_blacklisted=blacklisted_email is not None,
        blocked_reason=blacklisted_email.blocked_reason if blacklisted_email else None,
    )
