class ServiceError(Exception):
    pass


class MemeServiceError(ServiceError):
    pass


class DBServiceError(ServiceError):
    pass


class ImageServiceError(ServiceError):
    pass


class MemeNotFoundError(MemeServiceError, DBServiceError):
    pass


class ImageNotFoundError(ImageServiceError, DBServiceError):
    pass
