import base64
import logging

from internal.errors.errors import KeyDoesNotExistError, StorageServiceError
from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.storage_service_interface import StorageServiceInterface

logger = logging.getLogger(__name__)


class StorageService(StorageServiceInterface):
    storage_service_client: StorageServiceClientInterface

    def __init__(self, storage_service_client: StorageServiceClientInterface):
        self.storage_service_client = storage_service_client

    def create_data(self, key: str, b64_data: str):
        logger.info(f'Creating data with key: {key}')
        logger.debug(f'Creating data with key: {key}, B64 data: {b64_data}')

        data: bytes = base64.b64decode(b64_data)

        try:
            self.storage_service_client.create_data(
                key=key,
                data=data,
            )
        except StorageServiceError as e:
            logger.error(f"Failed to create data with key: {key}, error: {e}")
            raise

    def retrieve_data(self, key: str) -> str:
        logger.info(f'Retrieving data, key: {key}')

        try:
            data: bytes = self.storage_service_client.retrieve_data(
                key=key,
            )
        except KeyDoesNotExistError:
            logger.error(f'Failed to retrieve data for key: {key}, key does not exist')
            raise
        except StorageServiceError as e:
            logger.error(f'Failed to retrieve data for key: {key}, error: {e}')
            raise

        b64_data = base64.b64encode(data).decode('utf-8')

        logger.info(f'Retrieved data with key: {key}')
        logger.debug(f'Retrieved data with key: {key}, B64 data: {data}')

        return b64_data

    def delete_data(self, key: str):
        logger.info(f'Deleting data, key: {key}')

        try:
            self.storage_service_client.delete_data(
                key=key,
            )
        except KeyDoesNotExistError:
            logger.error(f'Failed to delete data for key: {key}, key does not exist')
            raise
        except StorageServiceError as e:
            logger.error(f'Failed to delete data for key: {key}, error: {e}')
            raise
