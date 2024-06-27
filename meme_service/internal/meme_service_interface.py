from abc import ABC, abstractmethod
from models.meme import Meme


class MemeServiceInterface(ABC):
    @abstractmethod
    def create_meme(self, meme: Meme):
        ...

    @abstractmethod
    def retrieve_meme(self, meme_id: str) -> Meme:
        ...

    @abstractmethod
    def retrieve_memes(self, skip: int, limit: int) -> list[Meme]:
        ...

    @abstractmethod
    def update_meme(self, meme_id: str, meme: Meme):
        ...

    @abstractmethod
    def delete_meme(self, meme_id: str):
        ...
