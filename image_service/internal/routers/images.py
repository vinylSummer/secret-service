from fastapi import APIRouter, status, HTTPException

from routers.dto.images import (CreateImageRequest, CreateImageResponse,
                                GetImageResponse,
                                UpdateImageRequest)
from internal.image_service_interface import ImageServiceInterface
from internal.errors.errors import ImageDoesNotExistError, ImageServiceError
from models.image import Image


def get_router(image_service: ImageServiceInterface) -> APIRouter:
    router = APIRouter(
        prefix="/images",
        tags=["images"],
    )

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateImageResponse)
    async def create_image(request: CreateImageRequest):
        image = request.to_model()

        try:
            image_service.create_image(image)
        except ImageServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return CreateImageResponse(
            image_id=image.image_id,
        )

    @router.get("/{image_id}")
    async def retrieve_image(image_id: str) -> GetImageResponse:
        try:
            image: Image = image_service.retrieve_image(image_id)
        except ImageDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ImageServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        return GetImageResponse(
            b64_data=image.b64_data,
        )

    # right now it's effectively the same as CREATE operation (overwrites existing data)
    # having a dedicated update handler will come in handy if image service functionality ever expands
    @router.put("/{image_id}")
    async def update_image(image_id: str, image_data: UpdateImageRequest):
        image_service.create_image(image_data.to_model(image_id))

    @router.delete("/{image_id}")
    async def delete_image(image_id: str):
        try:
            image_service.delete_image(image_id)
        except ImageDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ImageServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    return router
