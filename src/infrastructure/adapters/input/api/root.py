from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.domain.entities.managment import MessageResponse

router = APIRouter()


@router.get(
    "/",
    response_model=MessageResponse,
    tags=["management"],
    summary="Endpoint raiz",
    description="""Endpoint de verificación de salud del sistema.

   Devuelve un estado OK si el servicio está operativo y disponible.""",
    status_code=HTTPStatus.OK,
)
async def root() -> MessageResponse:
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal Server Error"
    )