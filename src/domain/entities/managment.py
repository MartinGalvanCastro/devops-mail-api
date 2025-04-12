from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """DTO de respuesta con un mensaje"""

    message: str = Field(
        ...,
        description="Mensaje descriptivo",
    )

    class Config:
        json_schema_extra = {
            "description": "Modelo de respuesta de un mensaje"
        }
