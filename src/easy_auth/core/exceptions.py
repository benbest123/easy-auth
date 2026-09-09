class AuthServiceError(Exception):
    pass


class ClientNotFoundError(AuthServiceError):
    pass
