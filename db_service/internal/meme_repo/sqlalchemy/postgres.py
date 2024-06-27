import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from internal.errors.errors import MemeDoesNotExistError, DatabaseError
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
        logger.info(f"Creating meme: {meme}")

        with self.session_maker() as session:
            try:
                session.add(meme)
            except IntegrityError as e:
                logger.error(f"Failed to create meme: {meme}, database Integrity Error: {e}")
                raise DatabaseError(
                    f'Failed to create meme: {meme.id}, integrity error: {e}'
                )
            except SQLAlchemyError as e:
                logger.error(f"Failed to create meme: {meme}, database error: {e}")
                raise DatabaseError(
                    f'Failed to create meme: {meme.id}, database error: {e}'
                )
            else:
                logger.info(f"Successfully created meme: {meme}")
                session.commit()

    def retrieve_meme(self, meme_id: str) -> Meme:
        logger.info(f"Retrieving meme: {meme_id}")

        with self.session_maker() as session:
            try:
                meme = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            except SQLAlchemyError as e:
                logger.error(f"Failed to retrieve meme: {meme_id}, database error: {e}")
                raise DatabaseError(
                    f'Failed to retrieve meme: {meme_id}, database error: {e}'
                )
            if meme is None:
                logger.error(f"Meme: {meme_id} does not exist in database")
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

            logger.info(f"Retrieved meme: {meme}")

            return meme

    def retrieve_memes(self, skip: int, limit: int) -> list[Meme]:
        logger.info(f"Retrieving memes: {skip=}, {limit=}")

        with self.session_maker() as session:
            try:
                memes = session.query(Meme).offset(skip).limit(limit).all()
            except SQLAlchemyError as e:
                logger.error(f"Failed to retrieve memes: {skip=}, {limit=}, database error: {e}")
                raise DatabaseError(
                    f'Failed to retrieve memes: {skip=}, {limit=}, database error: {e}'
                )
            if len(memes) == 0:
                logger.warning(f"No memes found with {skip=} and {limit=}")
                return []

            logger.info(f"Retrieved {len(memes)} memes with {skip=}, {limit=}: {memes}")

            return memes

    def update_meme(self, meme_id: str, meme: Meme):
        logger.info(f"Updating meme: {meme_id}, update: {meme}")

        with self.session_maker() as session:
            try:
                meme_to_update = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            except SQLAlchemyError as e:
                logger.error(f"Failed to update meme: {meme_id}, database error: {e}")
                raise DatabaseError(
                    f'Failed to update meme: {meme_id}, database error: {e}'
                )
            if meme_to_update is None:
                logger.error(f"Meme: {meme_id} does not exist in database")
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

            if meme.unique_meme_id is not None:
                logger.info(f"Updating meme: {meme_id}, new id: {meme.unique_meme_id}")
                meme_to_update.unique_meme_id = meme.unique_meme_id
            if meme.unique_image_id is not None:
                logger.info(f"Updating meme: {meme_id}, new image id: {meme.unique_image_id}")
                meme_to_update.unique_image_id = meme.unique_image_id
            if meme.caption is not None:
                logger.info(f"Updating meme: {meme_id}, new caption: {meme.caption}")
                meme_to_update.caption = meme.caption

            session.commit()

            logger.info(f"Updated meme: {meme_id}")

    def delete_meme(self, meme_id: str) -> Meme:
        logger.info(f"Deleting meme: {meme_id}")

        with self.session_maker() as session:
            try:
                meme = session.query(Meme).filter_by(unique_meme_id=meme_id).first()
            except SQLAlchemyError as e:
                logger.error(f"Failed to delete meme: {meme_id}, database error: {e}")
                raise DatabaseError(
                    f'Failed to delete meme: {meme_id}, database error: {e}'
                )
            if meme is None:
                logger.error(f"Meme: {meme_id} does not exist in database")
                raise MemeDoesNotExistError(f"Meme does not exist: {meme_id}")

            session.delete(meme)
            session.commit()

            logger.info(f"Deleted meme: {meme_id}")

            return meme
