import logging

from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.blacklists import (
    CreateBlacklistRequest,
    CreateBlacklistResponse,
    ValidateEmailInBlacklistResponse,
)
from src.infrastructure.adapters.output.db.session import get_async_session
from src.infrastructure.dependencies.services import get_blacklist_service

logger = logging.getLogger(__name__)

security = HTTPBearer()

router = APIRouter()


@router.post(
    "/blacklists",
    response_model=CreateBlacklistResponse,
    summary="Crear entrada en la lista negra",
    description="Crea una nueva entrada en la lista negra utilizando la dirección de correo electrónico, el identificador de la aplicación y la razón del bloqueo.",
    responses={
        401: {
            "description": "No se proporcionó un token de autenticación válido",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing or invalid authorization header"}
                }
            },
        }
    },
    # This adds the security scheme to the endpoint in Swagger UI.
)
async def create_blacklist(
    request: Request,
    data: CreateBlacklistRequest,
    session: AsyncSession = Depends(get_async_session),
    _token: HTTPAuthorizationCredentials = Security(security),
):
    """
    Creates a new blacklist entry using the provided data.

    This endpoint creates a blacklist record with the given email, app UUID,
    and blocked reason. The client's IP is captured from the request state.
    """
    service = get_blacklist_service(session=session)
    await service.create_blacklist(data=data, ip_address=request.state.client_ip)
    return CreateBlacklistResponse(message="Blacklist created successfully")


@router.get(
    "/blacklists/{email}",
    response_model=ValidateEmailInBlacklistResponse,
    summary="Validar correo en la lista negra",
    description="Valida si el correo electrónico está presente en la lista negra y devuelve la razón del bloqueo en caso de estarlo.",
    responses={
        401: {
            "description": "No se proporcionó un token de autenticación válido",
            "content": {
                "application/json": {
                    "example": {"detail": "Missing or invalid authorization header"}
                }
            },
        }
    },
)
async def validate_email_in_blacklist(
    email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
    _token: HTTPAuthorizationCredentials = Security(security),
):
    """
    Validates if a given email is present in the blacklist.

    This endpoint checks the presence of the email in the blacklist and returns
    whether it is blacklisted along with the blocked reason if applicable.
    """
    service = get_blacklist_service(session=session)
    blacklisted_email = await service.get_blacklist_by_email(email=str(email))
    return ValidateEmailInBlacklistResponse(
        is_blacklisted=blacklisted_email is not None,
        blocked_reason=blacklisted_email.blocked_reason
        if blacklisted_email
        else "User not blocked",
    )
