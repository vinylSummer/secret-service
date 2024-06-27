import requests
import logging

from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.errors.errors import StorageServiceError, KeyDoesNotExistError


logger = logging.getLogger(__name__)


class StorageServiceClient(StorageServiceClientInterface):
    storage_service_endpoint: str

    def __init__(self, storage_service_endpoint: str):
        self.storage_service_endpoint = storage_service_endpoint

    def create_data(self, key: str, b64_data: str):
        logger.info(f'Creating data with key: {key}')

        try:
            create_data_response = requests.post(
                self.storage_service_endpoint + "/",
                json={
                    "key": key,
                    "b64_data": b64_data,
                },
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to storage service: {self.storage_service_endpoint} failed. Error: {e}")
            raise StorageServiceError(f"Couldn't make the request: {e}")

        if create_data_response.status_code != 201:
            logger.error(
                f"Failed to create data with key: {key}, "
                f"code: {create_data_response.status_code}, "
                f"message: {create_data_response.text}"
            )
            raise StorageServiceError(
                f"Storage service error. "
                f"Code: {create_data_response.status_code} "
                f"Message: {create_data_response.text}"
            )

        logger.info(f"Created data with key: {key}")

    def retrieve_data(self, key: str) -> str:
        logger.info(f'Retrieving data with key: {key}')

        try:
            retrieve_data_response = requests.get(
                self.storage_service_endpoint + f"/{key}",
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to storage service: {self.storage_service_endpoint} failed. Error: {e}")
            raise StorageServiceError(f"Couldn't make the request: {e}")

        if retrieve_data_response.status_code == 404:
            raise KeyDoesNotExistError(
                f"Storage service error. "
                f"Code: {retrieve_data_response.status_code} "
                f"Message: {retrieve_data_response.text}"
            )

        if retrieve_data_response.status_code != 200:
            logger.error(
                f"Failed to create data with key: {key}, "
                f"code: {retrieve_data_response.status_code}, "
                f"message: {retrieve_data_response.text}"
            )
            raise StorageServiceError(
                f"Storage service error. "
                f"Code: {retrieve_data_response.status_code} "
                f"Message: {retrieve_data_response.text}"
            )

        b64_data = retrieve_data_response.json()["b64_data"]

        logger.info(f"Retrieved data with key: {key}")

        return b64_data

    def delete_data(self, key: str):
        logger.info(f'Deleting data with key: {key}')

        try:
            delete_data_response = requests.delete(
                self.storage_service_endpoint + f"/{key}",
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to storage service: {self.storage_service_endpoint} failed. Error: {e}")
            raise StorageServiceError(f"Couldn't make the request: {e}")

        if delete_data_response.status_code == 404:
            logger.error(f"Failed to delete data with key: {key}")
            raise KeyDoesNotExistError(
                f"Storage service error. "
                f"Code: {delete_data_response.status_code} "
                f"Message: {delete_data_response.text}"
            )

        if delete_data_response.status_code != 200:
            logger.error(
                f"Failed to create data with key: {key}, "
                f"code: {delete_data_response.status_code}, "
                f"message: {delete_data_response.text}"
            )
            raise StorageServiceError(
                f"Storage service error. "
                f"Code: {delete_data_response.status_code} "
                f"Message: {delete_data_response.text}"
            )

        logger.info(f"Deleted data with key: {key}")
