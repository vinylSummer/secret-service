class ServiceError(Exception):
    pass


class StorageServiceError(ServiceError):
    pass


class KeyDoesNotExistError(StorageServiceError):
    pass
