from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Blacklist(BaseModel):
    """Clase que representa una entrada en la lista negra"""

    id: UUID | None = Field(
        default=None,
        description="Identificador único para la entrada en la lista negra.",
    )
    email: EmailStr = Field(
        ...,
        max_length=255,
        description="Dirección de correo electrónico que se bloqueará.",
    )
    app_uuid: UUID = Field(
        ...,
        description="Identificador único de la aplicación asociada a la entrada en la lista negra.",
    )
    blocked_reason: str = Field(
        ...,
        max_length=255,
        description="Razón proporcionada para bloquear el correo electrónico.",
    )
    ip_address: str | None = Field(
        default=None,
        description="Dirección IP desde la cual se realizó la solicitud, si está disponible.",
    )
    created_at: datetime | None = Field(
        default=None,
        description="Fecha y hora en que se creó la entrada en la lista negra.",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Fecha y hora de la última actualización de la entrada en la lista negra.",
    )

    class Config:
        json_schema_extra = {"description": "Representa una entrada en la lista negra."}


class CreateBlacklistResponse(BaseModel):
    """DTO de respuesta de creacion de un correo en la lista negra."""

    message: str = Field(
        ...,
        description="Mensaje que indica el resultado después de crear la entrada en la lista negra.",
    )

    class Config:
        json_schema_extra = {
            "description": "Modelo de respuesta para la creación de una nueva entrada en la lista negra."
        }


class CreateBlacklistRequest(BaseModel):
    """DTO para crear un registro en la lista negra"""

    email: EmailStr = Field(
        ..., description="Dirección de correo electrónico que se bloqueará."
    )
    app_uuid: UUID = Field(
        ...,
        description="Identificador único de la aplicación para la cual se bloqueará el correo electrónico.",
    )
    blocked_reason: str = Field(
        ..., description="Razón por la cual se debe bloquear el correo electrónico."
    )

    class Config:
        json_schema_extra = {
            "description": "Modelo de solicitud para crear una nueva entrada en la lista negra."
        }


class ValidateEmailInBlacklistResponse(BaseModel):
    """DTO respuesta de checkeo de un email en la lista negra"""

    is_blacklisted: bool = Field(
        ...,
        description="Indica si el correo electrónico se encuentra en la lista negra.",
    )
    blocked_reason: str = Field(
        ...,
        description="Razón por la cual el correo electrónico fue bloqueado, si corresponde.",
    )

    class Config:
        json_schema_extra = {
            "description": "Modelo de respuesta para validar si un correo electrónico está en la lista negra."
        }
