from fastapi.testclient import TestClient

from easy_auth.core.config import get_settings


def test_read_jwks(client: TestClient) -> None:

    res = client.get("/.well-known/jwks.json")
    assert res.status_code == 200

    body = res.json()
    assert isinstance(body["keys"], list)

    key = body["keys"][0]

    assert key["crv"] == "Ed25519"
    assert key["kty"] == "OKP"
    assert key["kid"]

    assert (
        res.headers["cache-control"]
        == f"public, max-age={get_settings().jwks_cache_seconds}"
    )
