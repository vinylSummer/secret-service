class ServiceError(Exception):
    pass


class DBServiceError(ServiceError):
    pass


class DatabaseError(DBServiceError):
    pass


class MemeDoesNotExistError(DBServiceError):
    pass
