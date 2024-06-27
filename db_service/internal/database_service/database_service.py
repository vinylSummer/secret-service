import logging

from internal.database_service_interface import DatabaseServiceInterface
from internal.meme_repository_interface import MemeRepositoryInterface
from models.meme import Meme, MemeUpdate


logger = logging.getLogger(__name__)


class DatabaseService(DatabaseServiceInterface):
    meme_repo: MemeRepositoryInterface

    def __init__(self, meme_repository: MemeRepositoryInterface):
        self.meme_repo = meme_repository

    def create_meme(self, meme: Meme):
        logger.info(f'Creating meme: {meme}')

        try:
            self.meme_repo.create_meme(meme)
        except Exception as e:
            logger.error(e)
            raise

        logger.info(f'Created meme: {meme}')

    def retrieve_meme(self, meme_id: str) -> Meme:
        logger.info(f'Retrieving meme: {meme_id}')

        try:
            meme = self.meme_repo.retrieve_meme(meme_id)
        except Exception as e:
            logger.error(e)
            raise

        logger.info(f'Retrieved meme: {meme}')

        return meme

    def retrieve_memes(self, skip: int = 0, limit: int = 10) -> list[Meme]:
        logger.info(f'Retrieving memes: {skip=}, {limit=}')

        try:
            memes = self.meme_repo.retrieve_memes(skip, limit)
        except Exception as e:
            logger.error(e)
            raise

        logger.info(f'Retrieved {len(memes)} memes at {skip=}, {limit=}: {memes}')

        return memes

    def update_meme(self, meme_id: str, meme: MemeUpdate):
        logger.info(f'Updating meme: {meme_id}, update: {meme}')

        try:
            self.meme_repo.update_meme(meme_id, meme)
        except Exception as e:
            logger.error(e)
            raise

        logger.info(f'Updated meme: {meme_id}')

    def delete_meme(self, meme_id: str) -> Meme:
        logger.info(f'Deleting meme: {meme_id}')

        try:
            meme = self.meme_repo.delete_meme(meme_id)
        except Exception as e:
            logger.error(e)
            raise

        logger.info(f'Deleted meme: {meme_id}')

        return meme
