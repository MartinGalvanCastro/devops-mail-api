from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.domain.entities.managment import MessageResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=MessageResponse,
    tags=["management"],
    summary="Endpoint raiz",
    description="""Endpoint de verificación de salud del sistema.

   Devuelve un error 500 para simular una falla.""",
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
)
async def health() -> MessageResponse:
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal Server Error"
    )