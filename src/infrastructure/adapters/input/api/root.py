from fastapi import APIRouter

from src.domain.entities.managment import MessageResponse

router = APIRouter()


@router.get("/")
async def root()-> MessageResponse:
    return MessageResponse(message="OK")
