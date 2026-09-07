from fastapi import APIRouter, Response

from easy_auth.core.config import get_settings
from easy_auth.core.keys import JWKS, get_jwks

router = APIRouter()


@router.get("/.well-known/jwks.json")
def read_jwks(response: Response) -> JWKS:

    response.headers["Cache-Control"] = (
        f"public, max-age={get_settings().jwks_cache_seconds}"
    )
    return get_jwks()
