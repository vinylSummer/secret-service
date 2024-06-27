from internal.image_service_interface import ImageServiceInterface
from internal.s3_client_interface import S3ClientInterface
from internal.errors.errors import KeyDoesNotExistError, ImageDoesNotExistError
from models.image import Image


class ImageService(ImageServiceInterface):
    s3_client: S3ClientInterface

    def __init__(self, s3_client: S3ClientInterface):
        self.s3_client = s3_client

    def create_image(self, image: Image):
        self.s3_client.create_data(
            key=image.image_id,
            b64_data=image.b64_data,
        )

    def retrieve_image(self, image_id: str) -> Image:
        try:
            image_b64_data = self.s3_client.retrieve_data(
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
            self.s3_client.delete_data(
                key=image_id,
            )
        except KeyDoesNotExistError as e:
            raise ImageDoesNotExistError(e)
