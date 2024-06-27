import base64
import random

import pytest

from fastapi.testclient import TestClient
from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from internal.routers.dto.images import CreateImageRequest
from internal.routers import images

from internal.image_service_interface import ImageServiceInterface
from internal.image_service.image_service import ImageService
from internal.storage_service_client.fake_storage_service_client import FakeStorageServiceClient


@pytest.fixture(scope="function")
def s3_client():
    client = FakeStorageServiceClient()

    yield client


@pytest.fixture(scope="function")
def image_service(s3_client):
    service: ImageServiceInterface = ImageService(
        storage_service_client=s3_client
    )

    yield service


@pytest.fixture(scope='function')
def router(image_service) -> APIRouter:
    router = images.get_router(image_service)

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
            random_bytes: bytes = random.randbytes(1000)
            b64_string = base64.b64encode(random_bytes).decode()

            return b64_string

    yield B64StringFactory()


@pytest.fixture(scope='function')
def create_image_request_factory(b64_string_factory):
    class CreateMemeRequestFactory:
        def get(self):
            meme_b64_data: str = b64_string_factory.get()

            meme_request = CreateImageRequest(
                b64_data=meme_b64_data,
            )

            return meme_request

    yield CreateMemeRequestFactory()


class TestImageService:
    ROUTE_PREFIX = "/images"

    def create_images(self, test_client: TestClient, requests: list[CreateImageRequest]) -> list[str]:
        created_image_ids: list[str] = []
        for request in requests:
            response = test_client.post(
                self.ROUTE_PREFIX + "/",
                json=jsonable_encoder(request)
            )
            assert response.status_code == status.HTTP_201_CREATED
            created_image_ids.append(response.json().get("image_id"))

        return created_image_ids

    def test_create_image(self, client, create_image_request_factory):
        image1_request = create_image_request_factory.get()
        image2_request = create_image_request_factory.get()

        image1_id, image2_id = self.create_images(client, [image1_request, image2_request])

        response1 = client.get(
            self.ROUTE_PREFIX + f"/{image1_id}",
        )
        assert response1.status_code == status.HTTP_200_OK
        assert response1.json()["b64_data"] == image1_request.b64_data

        response2 = client.get(
            self.ROUTE_PREFIX + f"/{image2_id}"
        )
        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()["b64_data"] == image2_request.b64_data

        with pytest.raises(HTTPException):
            response3 = client.get(
                self.ROUTE_PREFIX + f"/idk",
            )
            assert response3.status_code == status.HTTP_404_NOT_FOUND

    def test_update_image(self, client, create_image_request_factory):
        image1_request = create_image_request_factory.get()
        image2_request = create_image_request_factory.get()

        image1_id, image2_id = self.create_images(client, [image1_request, image2_request])

        image3_request = create_image_request_factory.get()

        update_image1_response = client.put(
            self.ROUTE_PREFIX + f"/{image1_id}",
            json={"b64_data": image3_request.b64_data},
        )
        assert update_image1_response.status_code == status.HTTP_200_OK

        retrieve_image1_response = client.get(
            self.ROUTE_PREFIX + f"/{image1_id}"
        )
        assert retrieve_image1_response.status_code == status.HTTP_200_OK
        assert retrieve_image1_response.json()["b64_data"] == image3_request.b64_data

        retrieve_image2_response = client.get(
            self.ROUTE_PREFIX + f"/{image2_id}"
        )
        assert retrieve_image2_response.status_code == status.HTTP_200_OK
        assert retrieve_image2_response.json()["b64_data"] == image2_request.b64_data

    def test_delete_image(self, client, create_image_request_factory):
        image1_request = create_image_request_factory.get()
        image2_request = create_image_request_factory.get()

        image1_id, image2_id = self.create_images(client, [image1_request, image2_request])

        delete_image1_response = client.delete(
            self.ROUTE_PREFIX + f"/{image1_id}"
        )
        assert delete_image1_response.status_code == status.HTTP_200_OK

        with pytest.raises(HTTPException):
            retrieve_image1_response = client.get(
                self.ROUTE_PREFIX + f"/{image1_id}"
            )
            assert retrieve_image1_response.status_code == status.HTTP_404_NOT_FOUND

        retrieve_image2_response = client.get(
            self.ROUTE_PREFIX + f"/{image2_id}"
        )
        assert retrieve_image2_response.status_code == status.HTTP_200_OK
        assert retrieve_image2_response.json()["b64_data"] == image2_request.b64_data
