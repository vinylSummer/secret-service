from abc import ABC, abstractmethod


class StorageServiceClientInterface(ABC):
    @abstractmethod
    def create_data(self, key: str, data: bytes):
        ...

    @abstractmethod
    def retrieve_data(self, key: str) -> bytes:
        ...

    @abstractmethod
    def delete_data(self, key: str):
        ...
