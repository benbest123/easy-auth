import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from easy_auth.core.exceptions import ClientNotFoundError
from easy_auth.routers.auth import router as auth_router
from easy_auth.routers.jwks import router as jwks_router

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(jwks_router)
app.include_router(auth_router)


@app.exception_handler(ClientNotFoundError)
async def client_not_found_handler(
    request: Request, exc: ClientNotFoundError
) -> JSONResponse:

    logger.warning(str(exc))
    return JSONResponse(status_code=404, content={"detail": "client not found"})
