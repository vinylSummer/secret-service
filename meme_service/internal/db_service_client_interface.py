from abc import ABC, abstractmethod
from models.meme import DBMeme


class DatabaseServiceClientInterface(ABC):
    @abstractmethod
    def create_meme(self, meme: DBMeme):
        ...

    @abstractmethod
    def retrieve_meme(self, meme_id: str) -> DBMeme:
        ...

    @abstractmethod
    def retrieve_memes(self, skip: int, limit: int) -> list[DBMeme]:
        ...

    @abstractmethod
    def update_meme(self, meme_id: str, meme: DBMeme):
        ...

    @abstractmethod
    def delete_meme(self, meme_id: str) -> DBMeme:
        ...
