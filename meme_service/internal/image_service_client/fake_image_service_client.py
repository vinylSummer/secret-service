import uuid

from internal.image_service_client_interface import ImageServiceClientInterface
from internal.errors.errors import ImageNotFoundError


class FakeImageServiceClient(ImageServiceClientInterface):
    fake_storage: dict[str, str | None]

    def __init__(self):
        self.fake_storage = {}

    def create_image(self, b64_data: str) -> str:
        image_id = str(uuid.uuid4())
        self.fake_storage[image_id] = b64_data
        return image_id

    def retrieve_image(self, image_id: str) -> str:
        b64_data = self.fake_storage[image_id]
        return b64_data

    def update_image(self, image_id: str, b64_data: str):
        if image_id not in self.fake_storage.keys():
            raise ImageNotFoundError()

        self.fake_storage[image_id] = b64_data

    def delete_image(self, image_id: str):
        if image_id not in self.fake_storage.keys():
            raise ImageNotFoundError()

        del self.fake_storage[image_id]
