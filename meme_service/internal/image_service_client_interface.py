from abc import ABC, abstractmethod


class ImageServiceClientInterface(ABC):
    @abstractmethod
    def create_image(self, b64_data: str) -> str:
        ...

    @abstractmethod
    def retrieve_image(self, image_id: str) -> str:
        ...

    @abstractmethod
    def update_image(self, image_id: str, b64_data: str):
        ...

    @abstractmethod
    def delete_image(self, image_id: str) -> bool:
        ...
