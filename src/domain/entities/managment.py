from pydantic import BaseModel, ConfigDict, Field


class MessageResponse(BaseModel):
    """DTO de respuesta con un mensaje"""

    message: str = Field(
        ...,
        description="Mensaje descriptivo",
    )

    model_config = ConfigDict(
        json_schema_extra={"description": "Modelo de respuesta de un mensaje"}
    )
