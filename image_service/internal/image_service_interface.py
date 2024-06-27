from abc import ABC, abstractmethod
from models.image import Image


class ImageServiceInterface(ABC):
    @abstractmethod
    def create_image(self, image: Image):
        ...

    @abstractmethod
    def retrieve_image(self, image_id: str) -> Image:
        ...

    @abstractmethod
    def update_image(self, image: Image):
        ...

    @abstractmethod
    def delete_image(self, image_id: str):
        ...
