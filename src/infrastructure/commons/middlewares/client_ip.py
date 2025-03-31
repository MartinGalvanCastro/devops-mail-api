from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class ClientIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host

        request.state.client_ip = client_ip

        response = await call_next(request)
        return response
