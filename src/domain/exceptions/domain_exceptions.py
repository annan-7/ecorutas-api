class DomainError(Exception):
    """Base para errores esperados del dominio."""


class InvalidRouteError(DomainError):
    pass


class RouteNotFoundError(DomainError):
    pass


class DuplicateRouteError(DomainError):
    pass
