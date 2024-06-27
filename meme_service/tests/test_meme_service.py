import base64
import random

import pytest

from fastapi.testclient import TestClient
from fastapi import status, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from internal.routers.meme import get_router
from internal.routers.dto.meme import CreateMemeRequest, UpdateMemeRequest

from internal.meme_service_interface import MemeServiceInterface
from internal.meme_service.meme_service import MemeServiceV1
from internal.image_service_client_interface import ImageServiceClientInterface
from internal.image_service_client.fake_image_service_client import FakeImageServiceClient
from internal.db_service_client_interface import DatabaseServiceClientInterface
from internal.db_service_client.fake_db_service_client import FakeDatabaseServiceClient


@pytest.fixture(scope='function')
def db_client() -> DatabaseServiceClientInterface:
    client: DatabaseServiceClientInterface = FakeDatabaseServiceClient()

    yield client


@pytest.fixture(scope='function')
def image_client() -> ImageServiceClientInterface:
    client: ImageServiceClientInterface = FakeImageServiceClient()

    yield client


@pytest.fixture(scope='function')
def meme_service(db_client, image_client) -> MemeServiceInterface:
    service: MemeServiceInterface = MemeServiceV1(
        db_service_client=db_client,
        image_service_client=image_client,
    )

    yield service


@pytest.fixture(scope='function')
def router(meme_service) -> APIRouter:
    router = get_router(meme_service)

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
            random_bytes: bytes = random.randbytes(100)
            b64_string = base64.b64encode(random_bytes).decode()

            return b64_string

    yield B64StringFactory()


@pytest.fixture(scope='function')
def create_meme_request_factory(b64_string_factory):
    class CreateMemeRequestFactory:
        def get(self):
            meme_b64_data: str = b64_string_factory.get()
            meme_caption: str = b64_string_factory.get()

            meme_request = CreateMemeRequest(
                b64_data=meme_b64_data,
                caption=meme_caption
            )

            return meme_request

    yield CreateMemeRequestFactory()


class TestMemeService:
    ROUTE_PREFIX = "/memes"

    def create_memes(self, test_client, requests: list[CreateMemeRequest]) -> list[str]:
        meme_ids: list[str] = []
        for request in requests:
            response = test_client.post(
                self.ROUTE_PREFIX + "/",
                json=jsonable_encoder(request)
            )
            assert response.status_code == status.HTTP_201_CREATED
            meme_ids.append(response.json()["meme_id"])

        return meme_ids

    def test_create_meme(self, client, create_meme_request_factory):
        create_meme1_request = create_meme_request_factory.get()
        create_meme2_request = create_meme_request_factory.get()

        create_meme2_request.caption = None

        meme1_id, meme2_id = self.create_memes(client, [create_meme1_request, create_meme2_request])

        response1 = client.get(
            self.ROUTE_PREFIX + f"/{meme1_id}"
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json()["b64_data"] == create_meme1_request.b64_data
        assert response1.json()["caption"] == create_meme1_request.caption

        response2 = client.get(
            self.ROUTE_PREFIX + f"/{meme2_id}"
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()["b64_data"] == create_meme2_request.b64_data
        assert response2.json()["caption"] is None

    def test_retrieve_memes_paginated(self, client, create_meme_request_factory):
        meme1_request = create_meme_request_factory.get()
        meme2_request = create_meme_request_factory.get()
        meme3_request = create_meme_request_factory.get()

        meme_requests = [meme1_request, meme2_request, meme3_request]

        self.create_memes(
            client,
            meme_requests
        )

        skip = 0
        limit = 3
        all_memes_response = client.get(
            self.ROUTE_PREFIX + f"/?skip={skip}&limit={limit}",
        )
        assert all_memes_response.status_code == status.HTTP_200_OK
        assert len(all_memes_response.json()) == 3

        all_memes_response_json: list[dict[str, str]] = all_memes_response.json()
        for meme, meme_response in zip(meme_requests, all_memes_response_json):
            assert meme.b64_data == meme_response["b64_data"]
            assert meme.caption == meme_response["caption"]

        skip = 1
        limit = 3
        all_memes_response = client.get(
            self.ROUTE_PREFIX + f"/?skip={skip}&limit={limit}",
        )
        assert all_memes_response.status_code == status.HTTP_200_OK
        assert len(all_memes_response.json()) == 2

        meme_requests = meme_requests[1:]  # skip first meme
        all_memes_response_json: list[dict[str, str]] = all_memes_response.json()
        for meme, meme_response in zip(meme_requests, all_memes_response_json):
            assert meme.b64_data == meme_response["b64_data"]
            assert meme.caption == meme_response["caption"]

    def test_update_meme(self, client, create_meme_request_factory):
        meme1_request = create_meme_request_factory.get()
        meme2_request = create_meme_request_factory.get()

        meme_requests = [meme1_request, meme2_request]

        meme1_id, meme2_id = self.create_memes(
            client,
            meme_requests
        )

        meme2_updated_caption = "this caption was updated. nothing to see here"
        update_meme2_request = UpdateMemeRequest(
            caption=meme2_updated_caption
        )
        update_meme2_response = client.put(
            self.ROUTE_PREFIX + f"/{meme2_id}",
            json=jsonable_encoder(update_meme2_request)
        )
        assert update_meme2_response.status_code == status.HTTP_200_OK

        retrieve_meme2_response = client.get(
            self.ROUTE_PREFIX + f"/{meme2_id}"
        )
        assert retrieve_meme2_response.status_code == status.HTTP_200_OK
        assert retrieve_meme2_response.json()["b64_data"] == meme2_request.b64_data
        assert retrieve_meme2_response.json()["caption"] == meme2_updated_caption

        retrieve_meme1_response = client.get(
            self.ROUTE_PREFIX + f"/{meme1_id}"
        )
        assert retrieve_meme1_response.status_code == status.HTTP_200_OK
        assert retrieve_meme1_response.json()["b64_data"] == meme1_request.b64_data
        assert retrieve_meme1_response.json()["caption"] == meme1_request.caption

        update_meme1_request = UpdateMemeRequest()
        with pytest.raises(HTTPException):
            update_meme1_response = client.put(
                self.ROUTE_PREFIX + f"/{meme1_id}",
                json=jsonable_encoder(update_meme1_request)
            )
            assert update_meme1_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert update_meme1_response.json() == {}

        meme3_request = create_meme_request_factory.get()
        with pytest.raises(HTTPException):
            update_meme3_response = client.put(
                self.ROUTE_PREFIX + f"/very-fake-id",
                json=jsonable_encoder(meme3_request)
            )
            assert update_meme3_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_meme(self, client, create_meme_request_factory):
        meme1_request = create_meme_request_factory.get()
        meme2_request = create_meme_request_factory.get()

        meme_requests = [meme1_request, meme2_request]

        meme1_id, meme2_id = self.create_memes(
            client,
            meme_requests
        )

        delete_meme2_response = client.delete(
            self.ROUTE_PREFIX + f"/{meme2_id}"
        )
        assert delete_meme2_response.status_code == status.HTTP_200_OK

        with pytest.raises(HTTPException):
            retrieve_meme2_response = client.get(
                self.ROUTE_PREFIX + f"/{meme2_id}"
            )
            assert retrieve_meme2_response.status_code == status.HTTP_404_NOT_FOUND

        retrieve_meme1_response = client.get(
            self.ROUTE_PREFIX + f"/{meme1_id}"
        )
        assert retrieve_meme1_response.status_code == status.HTTP_200_OK
        assert retrieve_meme1_response.json()["b64_data"] == meme1_request.b64_data
        assert retrieve_meme1_response.json()["caption"] == meme1_request.caption
