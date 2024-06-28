from internal.errors.errors import KeyDoesNotExistError
from internal.storage_service_client_interface import StorageServiceClientInterface


class FakeStorageServiceClient(StorageServiceClientInterface):
    fake_storage: dict[str, bytes]

    def __init__(self):
        self.fake_storage = {}

    def create_data(self, key: str, data: bytes):
        self.fake_storage[key] = data

    def retrieve_data(self, key: str) -> bytes:
        if key in self.fake_storage.keys():
            return self.fake_storage[key]
        else:
            raise KeyDoesNotExistError()

    def delete_data(self, key: str):
        if key in self.fake_storage.keys():
            del self.fake_storage[key]
        else:
            raise KeyDoesNotExistError()
