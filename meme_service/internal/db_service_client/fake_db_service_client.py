from internal.db_service_client_interface import DatabaseServiceClientInterface
from internal.errors.errors import MemeNotFoundError
from models.meme import DBMeme


class FakeDatabaseServiceClient(DatabaseServiceClientInterface):
    fake_db: list[DBMeme]

    def __init__(self):
        self.fake_db = []

    def create_meme(self, meme: DBMeme):
        self.fake_db.append(meme)

    def retrieve_meme(self, meme_id: str) -> DBMeme:
        for meme in self.fake_db:
            if meme.id == meme_id:
                return meme
        raise MemeNotFoundError()

    def retrieve_memes(self, skip: int, limit: int) -> list[DBMeme]:
        memes = self.fake_db[skip: skip + limit]
        return memes

    def update_meme(self, meme_id: str, new_meme: DBMeme):
        for i, meme in enumerate(self.fake_db):
            if meme.id == meme_id:
                if new_meme.image_id:
                    self.fake_db[i].image_id = new_meme.image_id
                if new_meme.caption:
                    self.fake_db[i].caption = new_meme.caption

    def delete_meme(self, meme_id: str) -> DBMeme:
        for i, meme in enumerate(self.fake_db):
            if meme.id == meme_id:
                deleted_meme = self.fake_db.pop(i)
                return deleted_meme
        raise MemeNotFoundError()
