import traceback
from datetime import datetime

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.domain.entities.errors import (
    BaseErrorSchema,
    UnexpectedErrorSchema,
)
from src.domain.exceptions.base import CustomException


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=UnexpectedErrorSchema(
            error="unexpected_error",
            message=str(exc),
            details=traceback.format_exception(exc, value=exc, tb=exc.__traceback__),
            datetime=datetime.now().isoformat(),
        ).model_dump(),
    )


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code or 400,
        content=BaseErrorSchema(
            error=exc.error,
            message=exc.message,
            loc=None,
            input=None,
            ctx=None,
            datetime=datetime.now().isoformat(),
        ).model_dump(),
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=BaseErrorSchema(
            error=f"""{exc.errors()[0].get("type").lower()}""",
            message=f"""{exc.errors()[0].get("msg").lower()}""",
            loc=exc.errors()[0].get("loc"),
            input=exc.errors()[0].get("input"),
            ctx=exc.errors()[0].get("ctx"),
            datetime=datetime.now().isoformat(),
        ).model_dump(),
    )
