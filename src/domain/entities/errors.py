from typing import Any, Union

from pydantic import BaseModel, Field


class UnexpectedErrorSchema(BaseModel):
    """Schema for unexpected error responses."""

    error: str | None = Field(
        default=None, description="Código de error inesperado (si aplica)."
    )
    message: str | None = Field(
        default=None, description="Mensaje de error inesperado."
    )
    details: Any | None = Field(
        default=None, description="Detalles adicionales sobre el error."
    )
    datetime: str = Field(..., description="Fecha y hora en la que ocurrió el error.")

    class Config:
        json_schema_extra = {
            "description": "Esquema para errores inesperados en la API."
        }


class BaseErrorSchema(BaseModel):
    """Schema for base error responses."""

    error: str | None = Field(
        default=None, description="Código de error, si se proporciona."
    )
    message: str | None = Field(
        default=None, description="Mensaje descriptivo del error."
    )
    loc: Union[str, tuple] | None = Field(
        default=None, description="Localización (campo o posición) asociado al error."
    )
    input: Union[str, dict] | None = Field(
        default=None, description="Entrada de datos o payload que provocó el error."
    )
    ctx: dict | None = Field(
        default=None, description="Contexto adicional relacionado con el error."
    )
    datetime: str = Field(
        ..., description="Fecha y hora en la que se registró el error."
    )

    class Config:
        json_schema_extra = {"description": "Esquema base para respuestas de error."}
