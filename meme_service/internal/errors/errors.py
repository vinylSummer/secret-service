class ServiceError(Exception):
    """ Base class for all service errors """
    pass


class MemeServiceError(ServiceError):
    """ Base class for all meme service errors """
    pass


class DBServiceError(ServiceError):
    """ Base class for all database service errors """
    pass


class ImageServiceError(ServiceError):
    """ Base class for all image service errors """
    pass


class MemeNotFoundError(DBServiceError):
    """ Raised when a meme record is not found in database service """
    pass


class ImageNotFoundError(ImageServiceError):
    """ Raised when a meme image is not found in image service"""
    pass
