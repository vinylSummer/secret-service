import requests
import logging

from fastapi.encoders import jsonable_encoder

from internal.db_service_client_interface import DatabaseServiceClientInterface
from internal.errors.errors import DBServiceError, MemeNotFoundError
from internal.db_service_client.dto.meme import CreateMemeRequest
from models.meme import DBMeme


logger = logging.getLogger(__name__)


class DatabaseServiceClient(DatabaseServiceClientInterface):
    db_service_endpoint: str

    def __init__(self, db_service_endpoint):
        self.db_service_endpoint = db_service_endpoint

    def create_meme(self, meme: DBMeme):
        request_body = CreateMemeRequest(
            meme_id=meme.id,
            image_id=meme.image_id,
            caption=meme.caption,
        )
        try:
            create_meme_response = requests.post(
                self.db_service_endpoint + "/",
                json=jsonable_encoder(request_body),
            )
        except requests.exceptions.RequestException as e:
            raise DBServiceError(f"Couldn't make the request: {e}")

        if create_meme_response.status_code != 201:
            raise DBServiceError(
                f"{create_meme_response.status_code}: {create_meme_response.text}"
            )

    def retrieve_meme(self, meme_id: str) -> DBMeme:
        logger.info(f"Retrieving meme: {meme_id}")

        try:
            retrieve_meme_response = requests.get(
                self.db_service_endpoint + f"/{meme_id}",
            )
        except requests.exceptions.RequestException as e:
            raise DBServiceError(f"Couldn't make the request: {e}")

        if retrieve_meme_response.status_code == 404:
            raise MemeNotFoundError()

        if retrieve_meme_response.status_code != 200:
            raise DBServiceError(
                f"{retrieve_meme_response.status_code}: {retrieve_meme_response.text}"
            )

        response_json = retrieve_meme_response.json()
        meme = DBMeme(
            id=meme_id,
            image_id=response_json["image_id"],
            caption=response_json["caption"],
        )

        logger.info(f"Retrieved meme: {meme}")

        return meme

    def retrieve_memes(self, skip: int, limit: int) -> list[DBMeme]:
        logger.info(f"Retrieving memes: {skip=}, {limit=}")

        params = {
            "skip": skip,
            "limit": limit,
        }
        try:
            retrieve_memes_response = requests.get(
                self.db_service_endpoint + "/",
                params=params,
            )
        except requests.exceptions.RequestException as e:
            raise DBServiceError(f"Couldn't make the request: {e}")

        if retrieve_memes_response.status_code == 404:
            return []

        if retrieve_memes_response.status_code != 200:
            raise DBServiceError(
                f"{retrieve_memes_response.status_code}: {retrieve_memes_response.text}"
            )

        db_memes: list[DBMeme] = []
        response_json = retrieve_memes_response.json()
        for meme in response_json:
            db_memes.append(
                DBMeme(
                    id=meme["meme_id"],
                    image_id=meme["image_id"],
                    caption=meme["caption"],
                )
            )

        logger.info(f"Retrieved {len(db_memes)} memes for {skip=}, {limit=}: {db_memes}")

        return db_memes

    def update_meme(self, meme_id: str, meme: DBMeme):
        logger.info(f"Updating meme: {meme_id}, update: {meme}")

        try:
            update_meme_response = requests.put(
                self.db_service_endpoint + f"/{meme_id}",
                json=jsonable_encoder(meme),
            )
        except requests.exceptions.RequestException as e:
            raise DBServiceError(f"Couldn't make the request: {e}")

        if update_meme_response.status_code == 404:
            raise MemeNotFoundError()

        if update_meme_response.status_code != 200:
            raise DBServiceError(
                f"{update_meme_response.status_code}: {update_meme_response.text}"
            )

        logger.info(f"Successfully updated meme: {meme_id}")

    def delete_meme(self, meme_id: str) -> DBMeme:
        logger.info(f"Deleting meme: {meme_id}")

        try:
            delete_meme_response = requests.delete(
                self.db_service_endpoint + f"/{meme_id}",
            )
        except requests.exceptions.RequestException as e:
            raise DBServiceError(f"Couldn't make the request: {e}")

        if delete_meme_response.status_code == 404:
            raise MemeNotFoundError()

        if delete_meme_response.status_code != 200:
            raise DBServiceError(
                f"{delete_meme_response.status_code}: {delete_meme_response.text}"
            )

        deleted_meme = DBMeme(
            id=delete_meme_response.json()["meme_id"],
            image_id=delete_meme_response.json()["image_id"],
            caption=delete_meme_response.json()["caption"],
        )

        logger.info(f"Successfully deleted meme: {meme_id}")

        return deleted_meme
