class ServiceError(Exception):
    pass


class DBServiceError(ServiceError):
    pass


class MemeDoesNotExistError(DBServiceError):
    pass
