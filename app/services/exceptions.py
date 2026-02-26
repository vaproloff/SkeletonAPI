class ServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(ServiceError):
    pass


class AlreadyExistsError(ServiceError):
    pass
