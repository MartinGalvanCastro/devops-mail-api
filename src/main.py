from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions.base import CustomException
from src.infrastructure.commons.errors.handlers import (
    custom_exception_handler,
    exception_handler,
    request_validation_exception_handler,
)
from src.infrastructure.commons.logger.base import setup_logging
from src.infrastructure.commons.middlewares.client_ip import ClientIPMiddleware
from src.infrastructure.commons.middlewares.jwt import JWTMiddleware
from src.infrastructure.commons.settings.base import settings
from src.routes import router_v1
from src.infrastructure.adapters.input.api.root import router as root_router
from src.infrastructure.adapters.input.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    dependencies=[],
    proxies={"X-Forwarded-For"},
)

app.add_middleware(ClientIPMiddleware)
app.add_middleware(JWTMiddleware)

app.include_router(router_v1)
app.include_router(root_router)
app.include_router(health_router)

app.exception_handler(Exception)(exception_handler)
app.exception_handler(CustomException)(custom_exception_handler)
app.exception_handler(RequestValidationError)(request_validation_exception_handler)
