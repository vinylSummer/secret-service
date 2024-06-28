import base64
import random

import pytest
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from internal.routes.data import get_router
from internal.routes.dto.data import CreateDataRequest
from internal.storage_service.storage_service import StorageService
from internal.storage_service_client.fake_storage_service_client import FakeStorageServiceClient
from internal.storage_service_client_interface import StorageServiceClientInterface
from internal.storage_service_interface import StorageServiceInterface


@pytest.fixture(scope='function')
def storage_service_client() -> StorageServiceClientInterface:
    client: StorageServiceClientInterface = FakeStorageServiceClient()

    yield client


@pytest.fixture(scope='function')
def storage_service(storage_service_client: StorageServiceClientInterface) -> StorageServiceInterface:
    service: StorageServiceInterface = StorageService(
        storage_service_client=storage_service_client,
    )

    yield service


@pytest.fixture(scope='function')
def router(storage_service) -> APIRouter:
    router = get_router(storage_service)

    yield router


@pytest.fixture(scope='function')
def client(router) -> TestClient:
    _client = TestClient(router)

    yield _client

    _client.close()


@pytest.fixture(scope='function')
def b64_string_factory():
    random.seed(1)

    class B64StringFactory:
        def get(self):
            random_bytes: bytes = random.randbytes(10)
            b64_string = base64.b64encode(random_bytes).decode()

            return b64_string

    yield B64StringFactory()


@pytest.fixture(scope='function')
def create_data_request_factory(b64_string_factory):
    class CreateDataRequestFactory:
        def get(self):
            key = b64_string_factory.get()
            b64_data = b64_string_factory.get()

            data_request = CreateDataRequest(
                key=key,
                b64_data=b64_data,
            )

            return data_request

    yield CreateDataRequestFactory()


class TestS3Service:
    ROUTE_PREFIX = "/data"

    def create_data(self, test_client, requests: list[CreateDataRequest]):
        for request in requests:
            response = test_client.post(
                self.ROUTE_PREFIX + "/",
                json=jsonable_encoder(request)
            )
            assert response.status_code == status.HTTP_201_CREATED

    def test_data_upload(self, client, create_data_request_factory):
        create_data1_request = create_data_request_factory.get()
        create_data2_request = create_data_request_factory.get()

        self.create_data(client, [create_data1_request, create_data2_request])

        response1 = client.get(
            self.ROUTE_PREFIX + f"/{create_data1_request.key}"
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json()['b64_data'] == create_data1_request.b64_data

        response2 = client.get(
            self.ROUTE_PREFIX + f"/{create_data2_request.key}"
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()['b64_data'] == create_data2_request.b64_data

    def test_data_deletion(self, client, create_data_request_factory):
        create_data1_request = create_data_request_factory.get()
        create_data2_request = create_data_request_factory.get()

        self.create_data(client, [create_data1_request, create_data2_request])

        delete_data1_response = client.delete(
            self.ROUTE_PREFIX + f"/{create_data1_request.key}"
        )
        assert delete_data1_response.status_code == status.HTTP_200_OK

        with pytest.raises(HTTPException):
            delete_data1_response = client.delete(
                self.ROUTE_PREFIX + f"/{create_data1_request.key}"
            )
            assert delete_data1_response.status_code == status.HTTP_404_NOT_FOUND

        with pytest.raises(HTTPException):
            retrieve_data1_response = client.get(
                self.ROUTE_PREFIX + f"/{create_data1_request.key}"
            )
            assert retrieve_data1_response.status_code == status.HTTP_404_NOT_FOUND

        retrieve_data2_response = client.get(
            self.ROUTE_PREFIX + f"/{create_data2_request.key}"
        )
        assert retrieve_data2_response.status_code == status.HTTP_200_OK
        assert retrieve_data2_response.json()['b64_data'] == create_data2_request.b64_data
