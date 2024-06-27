from internal.meme_repository_interface import MemeRepositoryInterface
from internal.errors.errors import MemeDoesNotExistError
from models.meme import Meme, MemeUpdate


class FakeMemeRepository(MemeRepositoryInterface):
    fake_db: list[Meme]

    def __init__(self):
        self.fake_db = []

    def create_meme(self, meme: Meme):
        self.fake_db.append(meme)

    def retrieve_meme(self, meme_id: str) -> Meme:
        for meme in self.fake_db:
            if meme.unique_meme_id == meme_id:
                return meme
        else:
            raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

    def retrieve_memes(self, skip: int, limit: int) -> list[Meme]:
        start = skip
        end = skip + limit

        max_index = len(self.fake_db)
        if start > max_index:
            return []
        if end > max_index:
            end = max_index

        memes = self.fake_db[start:end]

        return memes

    def update_meme(self, meme_id: str, new_meme: MemeUpdate):
        for i, meme in enumerate(self.fake_db):
            if meme.unique_meme_id == meme_id:
                if new_meme.unique_image_id:
                    self.fake_db[i].unique_image_id = new_meme.unique_image_id
                if new_meme.caption:
                    self.fake_db[i].caption = new_meme.caption
                return
        else:
            raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

    def delete_meme(self, meme_id: str) -> Meme:
        for i, meme in enumerate(self.fake_db):
            if meme.unique_meme_id == meme_id:
                return self.fake_db.pop(i)
        else:
            raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")
