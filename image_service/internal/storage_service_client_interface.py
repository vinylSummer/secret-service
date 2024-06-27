from abc import ABC, abstractmethod


class StorageServiceClientInterface(ABC):
    @abstractmethod
    def create_data(self, key: str, b64_data: str):
        ...

    @abstractmethod
    def retrieve_data(self, key: str) -> str:
        ...

    @abstractmethod
    def delete_data(self, key: str):
        ...
