from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.errors.errors import KeyDoesNotExistError


class FakeStorageServiceClient(StorageServiceClientInterface):
    fake_storage: dict[str, str]

    def __init__(self):
        self.fake_storage = {}

    def create_data(self, key: str, b64_data: str):
        self.fake_storage[key] = b64_data

    def retrieve_data(self, key: str) -> str:
        data = self.fake_storage.get(key)
        if data is None:
            raise KeyDoesNotExistError(f"Key {key} does not exist")

        return data

    def delete_data(self, key: str):
        if key not in self.fake_storage.keys():
            raise KeyDoesNotExistError(f"Key {key} does not exist")

        del self.fake_storage[key]
