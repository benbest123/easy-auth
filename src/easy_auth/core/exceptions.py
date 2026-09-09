class AuthServiceError(Exception):
    pass


class ClientNotFoundError(AuthServiceError):
    pass


class ClientInactiveError(ClientNotFoundError):
    # distinct from ClientNotFoundError
    # both return 404, but useful for logging 'client X exists but is not active'
    pass
