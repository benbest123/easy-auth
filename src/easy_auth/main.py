from fastapi import FastAPI

from easy_auth.routers.jwks import router as jwks_router

app = FastAPI()

app.include_router(jwks_router)
