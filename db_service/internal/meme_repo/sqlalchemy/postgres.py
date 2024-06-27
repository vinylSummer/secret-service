import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from internal.errors.errors import MemeDoesNotExistError, DBServiceError
from internal.meme_repository_interface import MemeRepositoryInterface
from internal.postgres.connection import PostgresConnection
from models.meme import Meme

logger = logging.getLogger(__name__)


# noinspection PyTypeChecker, orm type hints the return as Type[X] instead of X
class MemeRepository(MemeRepositoryInterface):
    db_connection: PostgresConnection
    session_maker: sessionmaker

    def __init__(self, db_connection: PostgresConnection):
        self.db_connection = db_connection
        self.session_maker = sessionmaker(
            bind=self.db_connection.engine,
            autocommit=False,
            autoflush=False,
        )

    def create_meme(self, meme: Meme):
        with self.session_maker() as session:
            try:
                session.add(meme)
            except IntegrityError:
                raise DBServiceError(
                    f'Meme already exists in database: {meme.id}'
                )
            else:
                session.commit()

    def retrieve_meme(self, meme_id: str) -> Meme:
        with self.session_maker() as session:
            meme = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            if meme is None:
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

            return meme

    def retrieve_memes(self, skip: int, limit: int) -> list[Meme]:
        with self.session_maker() as session:
            memes = session.query(Meme).offset(skip).limit(limit).all()
            if len(memes) == 0:
                logger.info(f"No memes found with {skip=} and {limit=}")
                return []
            return memes

    def update_meme(self, meme_id: str, meme: Meme):
        with self.session_maker() as session:
            meme_to_update = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            if meme_to_update is None:
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

            if meme.unique_meme_id is not None:
                meme_to_update.unique_meme_id = meme.unique_meme_id
            if meme.unique_image_id is not None:
                meme_to_update.unique_image_id = meme.unique_image_id
            if meme.caption is not None:
                meme_to_update.caption = meme.caption

            session.commit()

    def delete_meme(self, meme_id: str) -> Meme:
        with self.session_maker() as session:
            meme = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            if meme is None:
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")
            session.delete(meme)
            session.commit()

            return meme
