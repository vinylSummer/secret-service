import logging

from internal.image_service_interface import ImageServiceInterface
from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.errors.errors import KeyDoesNotExistError, ImageDoesNotExistError, StorageServiceError, ServiceError
from models.image import Image


logger = logging.getLogger(__name__)


class ImageService(ImageServiceInterface):
    storage_service_client: StorageServiceClientInterface

    def __init__(self, storage_service_client: StorageServiceClientInterface):
        self.storage_service_client = storage_service_client

    def create_image(self, image: Image):
        logger.info(f'Creating image with id: {image.image_id}')

        self.storage_service_client.create_data(
            key=image.image_id,
            b64_data=image.b64_data,
        )

        logger.info(f'Created image with id: {image.image_id}')

    def retrieve_image(self, image_id: str) -> Image:
        logger.info(f'Retrieving image with id: {image_id}')

        try:
            image_b64_data = self.storage_service_client.retrieve_data(
                key=image_id,
            )
        except KeyDoesNotExistError as e:
            logger.error(f'Image with id: {image_id} does not exist')
            raise ImageDoesNotExistError(e)
        except StorageServiceError as e:
            logger.error(f"Couldn't retrieve image with id: {image_id}, storage service error: {e}")
            raise

        logger.info(f'Retrieved image with id: {image_id}')

        return Image(
            image_id=image_id,
            b64_data=image_b64_data,
        )

    def update_image(self, image: Image):
        logger.info(f'Updating image with id: {image.image_id}')

        try:
            self.create_image(image)
        except ServiceError as e:
            logger.error(f"Couldn't update image with id: {image.image_id}, service error: {e}")
            raise

        logger.info(f"Updated image with id: {image.image_id}")

    def delete_image(self, image_id: str):
        logger.info(f'Deleting image with id: {image_id}')

        try:
            self.storage_service_client.delete_data(
                key=image_id,
            )
        except KeyDoesNotExistError as e:
            logger.error(f"Failed to delete image with id: {image_id}. Image does not exist")
            raise ImageDoesNotExistError(e)
        except StorageServiceError as e:
            logger.error(f"Couldn't delete image with id: {image_id}, storage service error: {e}")
            raise

        logger.info(f"Deleted image with id: {image_id}")
