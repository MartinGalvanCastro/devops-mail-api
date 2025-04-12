from fastapi import APIRouter

from src.infrastructure.adapters.input.api.blacklist import router as blacklist_router

router_v1 = APIRouter()

router_v1.include_router(blacklist_router, tags=["blacklist"])
