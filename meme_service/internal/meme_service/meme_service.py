import logging

from internal.meme_service_interface import MemeServiceInterface
from internal.db_service_client_interface import DatabaseServiceClientInterface
from internal.image_service_client_interface import ImageServiceClientInterface
from internal.errors.errors import DBServiceError, ImageServiceError, MemeNotFoundError, ImageNotFoundError
from models.meme import DBMeme, Meme


logger = logging.getLogger(__name__)


class MemeServiceV1(MemeServiceInterface):
    db_service_client: DatabaseServiceClientInterface
    image_service_client: ImageServiceClientInterface

    def __init__(
        self,
        db_service_client: DatabaseServiceClientInterface,
        image_service_client: ImageServiceClientInterface,
    ):
        self.db_service_client = db_service_client
        self.image_service_client = image_service_client

    def create_meme(self, meme: Meme):
        logger.info(f"Creating meme: {meme}")

        try:
            image_id: str = self.image_service_client.create_image(
                meme.b64_data
            )
        except ImageServiceError as e:
            logger.error(f"Failed to create image for {meme}, error: {e}")
            raise

        try:
            self.db_service_client.create_meme(
                DBMeme(
                    id=meme.id,
                    image_id=image_id,
                    caption=meme.caption,
                )
            )
        except DBServiceError as e:
            logger.error(f"Failed to create database record for {meme}, error: {e}")
            raise

        logger.info(f"Created meme: {meme}")

    def retrieve_meme(self, meme_id: str):
        logger.info(f"Retrieving meme: {meme_id}")

        try:
            db_meme: DBMeme = self.db_service_client.retrieve_meme(
                meme_id
            )
        except MemeNotFoundError:
            logger.error(f"Meme not found: {meme_id}")
            raise
        except DBServiceError as e:
            logger.error(f"Failed to retrieve database record for {meme_id} meme id, error: {e}")
            raise

        try:
            image_b64data = self.image_service_client.retrieve_image(
                db_meme.image_id
            )
        except ImageNotFoundError:
            logger.error(f"Image not found: {db_meme.image_id}, even though there is a database record for it!")
            raise
        except ImageServiceError as e:
            logger.error(f"Failed to retrieve image for {db_meme}, error: {e}")
            raise

        meme = Meme(
            id=db_meme.id,
            b64_data=image_b64data,
            caption=db_meme.caption,
        )

        logger.info(f"Successfully retrieved meme: {meme}")

        return meme

    def retrieve_memes(self, skip: int, limit: int) -> list[Meme]:
        logger.info(f"Retrieving memes: {skip=}, {limit=}")

        try:
            db_memes = self.db_service_client.retrieve_memes(
                skip,
                limit,
            )
        except DBServiceError as e:
            logger.error(f"Failed to retrieve database records for memes. {skip=} {limit=}, error: {e}")
            raise

        logger.info(f"Successfully retrieved db meme records: {db_memes}")

        memes: list[Meme] = []
        for db_meme in db_memes:
            try:
                meme_image = self.image_service_client.retrieve_image(
                    db_meme.image_id
                )
            except ImageServiceError as e:
                logger.error(f"Failed to retrieve image for {db_meme}, error: {e}")
                raise
            memes.append(
                Meme(
                    id=db_meme.id,
                    b64_data=meme_image,
                    caption=db_meme.caption,
                )
            )

        logger.info(f"Retrieved {len(memes)} meme images for {skip=}, {limit=}. Completed memes: {memes}")

        return memes

    def update_meme(self, meme_id: str, meme: Meme):
        logger.info(f"Updating meme: {meme_id}, update: {meme}")

        try:
            db_meme = self.db_service_client.retrieve_meme(
                meme_id
            )
        except DBServiceError as e:
            logger.error(f"Failed to retrieve database record for {meme}, error: {e}")
            raise

        logger.info(f"Successfully retrieved database record for {meme_id}: {db_meme}")

        if meme.caption:
            logger.info(f"Updating caption for {meme_id}: {db_meme.caption} -> {meme.caption}")

            db_meme.caption = meme.caption
            try:
                self.db_service_client.update_meme(
                    meme_id,
                    db_meme
                )
            except DBServiceError as e:
                logger.error(f"Failed to update database record for {meme}, error: {e}")
                raise

            logger.info(f"Successfully updated caption for {meme_id}")

        if meme.b64_data != "":
            logger.info(f"Updating b64 data for {meme_id}")

            try:
                self.image_service_client.update_image(
                    db_meme.image_id,
                    meme.b64_data,
                )
            except ImageServiceError as e:
                logger.error(f"Failed to update image for {db_meme}, error: {e}")
                raise

            logger.info(f"Successfully updated b64 data for {meme_id}")

        logger.info(f"Successfully updated meme: {meme_id}")

    def delete_meme(self, meme_id: str):
        logger.info(f"Deleting meme: {meme_id}")

        try:
            deleted_db_meme = self.db_service_client.delete_meme(
                meme_id
            )
        except DBServiceError as e:
            logger.error(f"Failed to delete database record for {meme_id}, error: {e}")
            raise

        try:
            self.image_service_client.delete_image(
                deleted_db_meme.image_id
            )
        except ImageServiceError as e:
            logger.error(f"Failed to delete image for {deleted_db_meme}, error: {e}")
            raise

        logger.info(f"Successfully deleted meme: {meme_id}")
