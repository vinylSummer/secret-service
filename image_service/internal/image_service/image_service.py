from internal.image_service_interface import ImageServiceInterface
from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.errors.errors import KeyDoesNotExistError, ImageDoesNotExistError
from models.image import Image


class ImageService(ImageServiceInterface):
    storage_service_client: StorageServiceClientInterface

    def __init__(self, storage_service_client: StorageServiceClientInterface):
        self.storage_service_client = storage_service_client

    def create_image(self, image: Image):
        self.storage_service_client.create_data(
            key=image.image_id,
            b64_data=image.b64_data,
        )

    def retrieve_image(self, image_id: str) -> Image:
        try:
            image_b64_data = self.storage_service_client.retrieve_data(
                key=image_id,
            )
        except KeyDoesNotExistError as e:
            raise ImageDoesNotExistError(e)

        return Image(
            image_id=image_id,
            b64_data=image_b64_data,
        )

    def update_image(self, image: Image):
        self.create_image(image)

    def delete_image(self, image_id: str):
        try:
            self.storage_service_client.delete_data(
                key=image_id,
            )
        except KeyDoesNotExistError as e:
            raise ImageDoesNotExistError(e)
