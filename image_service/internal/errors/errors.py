class ServiceError(Exception):
    """ Base class for all service errors """
    pass


class StorageServiceError(ServiceError):
    """ Raised when an error occurs in S3 client """
    pass


class ImageServiceError(ServiceError):
    """ Raised when an error occurs in image service """
    pass


class KeyDoesNotExistError(StorageServiceError):
    """ Raised when a key does not exist in storage service """
    pass


class ImageDoesNotExistError(ImageServiceError):
    """ Raised when an image does not exist in image service """
    pass
