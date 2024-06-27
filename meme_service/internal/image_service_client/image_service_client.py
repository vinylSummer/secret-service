import requests

from fastapi.encoders import jsonable_encoder

from internal.image_service_client_interface import ImageServiceClientInterface
from internal.image_service_client.dto.image import CreateImageRequest, UpdateImageRequest
from internal.errors.errors import ImageNotFoundError, ImageServiceError


class ImageServiceClient(ImageServiceClientInterface):
    image_service_endpoint: str

    def __init__(self, image_service_endpoint: str):
        self.image_service_endpoint = image_service_endpoint

    def create_image(self, b64_data: str) -> str:
        request_body = CreateImageRequest(
            b64_data=b64_data,
        )
        try:
            create_image_response = requests.post(
                self.image_service_endpoint + "/",
                json=jsonable_encoder(request_body)
            )
        except requests.exceptions.RequestException as e:
            raise ImageServiceError(f"Couldn't make the request: {e}")

        if create_image_response.status_code != 201:
            raise ImageServiceError(
                f"{create_image_response.status_code}: {create_image_response.text}"
            )

        image_id: str = create_image_response.json().get('image_id')

        return image_id

    def retrieve_image(self, image_id: str) -> str:
        try:
            retrieve_image_response = requests.get(
                self.image_service_endpoint + f"/{image_id}",
            )
        except requests.exceptions.RequestException as e:
            raise ImageServiceError(f"Couldn't make the request: {e}")

        if retrieve_image_response.status_code == 404:
            raise ImageNotFoundError(
                f"{retrieve_image_response.status_code}: {retrieve_image_response.text}"
            )

        if retrieve_image_response.status_code != 200:
            raise ImageServiceError(
                f"{retrieve_image_response.status_code}: {retrieve_image_response.text}"
            )

        image_b64_data: str = retrieve_image_response.json().get('b64_data')

        return image_b64_data

    def update_image(self, image_id: str, b64_data: str):
        request_body = UpdateImageRequest(
            b64_data=b64_data,
        )
        try:
            update_image_response = requests.put(
                self.image_service_endpoint + f"/{image_id}",
                json=jsonable_encoder(request_body)
            )
        except requests.exceptions.RequestException as e:
            raise ImageServiceError(f"Couldn't make the request: {e}")

        if update_image_response.status_code == 404:
            raise ImageNotFoundError(
                f"{update_image_response.status_code}: {update_image_response.text}"
            )

        if update_image_response.status_code != 200:
            raise ImageServiceError(
                f"{update_image_response.status_code}: {update_image_response.text}"
            )

    def delete_image(self, image_id: str):
        try:
            delete_image_response = requests.delete(
                self.image_service_endpoint + f"/{image_id}",
            )
        except requests.exceptions.RequestException as e:
            raise ImageServiceError(f"Couldn't make the request: {e}")

        if delete_image_response.status_code == 404:
            raise ImageNotFoundError(
                f"{delete_image_response.status_code}: {delete_image_response.text}"
            )

        if delete_image_response.status_code != 200:
            raise ImageServiceError(
                f"{delete_image_response.status_code}: {delete_image_response.text}"
            )
