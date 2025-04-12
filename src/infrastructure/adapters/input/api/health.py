from fastapi import APIRouter

from src.domain.entities.managment import MessageResponse

router = APIRouter()


@router.get("/health")
async def health() -> MessageResponse:
    return MessageResponse(message="OK")
