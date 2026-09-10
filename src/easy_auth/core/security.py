import secrets
from functools import lru_cache

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password=password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hash=hashed, password=password)
        return True

    except VerifyMismatchError:
        return False


# dummy hash so response time doesnt reveal account existence
@lru_cache
def dummy_hash() -> str:
    return ph.hash(secrets.token_urlsafe(32))


def needs_rehash(hashed: str) -> bool:
    return ph.check_needs_rehash(hashed)
