class AuthServiceError(Exception):
    pass


class ClientNotFoundError(AuthServiceError):
    pass


class EmailAlreadyRegisteredError(AuthServiceError):
    pass


class ClientInactiveError(AuthServiceError):
    pass


class NoAutoProvisionError(AuthServiceError):
    pass
