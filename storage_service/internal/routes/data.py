import logging

from fastapi import APIRouter, status, HTTPException

from internal.errors.errors import KeyDoesNotExistError, StorageServiceError
from internal.routes.dto.data import CreateDataRequest, RetrieveDataResponse
from internal.storage_service_interface import StorageServiceInterface

logger = logging.getLogger(__name__)


def get_router(s3_service: StorageServiceInterface) -> APIRouter:
    router = APIRouter(
        prefix="/data",
        tags=["data"],
    )

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_data(request: CreateDataRequest):
        logger.info(f"Creating data, request: {request}")

        try:
            s3_service.create_data(request.key, request.b64_data)
        except StorageServiceError as e:
            logger.error(f"Failed to create data for request: {request}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Created data for request: {request}")

    @router.get("/{key}")
    async def retrieve_data(key: str) -> RetrieveDataResponse:
        logger.info(f"Retrieving data, key: {key}")

        try:
            b64_data: str = s3_service.retrieve_data(key)
        except KeyDoesNotExistError:
            logger.error(f"Failed to retrieve key: {key}, does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except StorageServiceError as e:
            logger.error(f"Failed to retrieve key: {key}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        logger.info(f"Retrieved data for key: {key}")
        logger.debug(f"Retrieved data for key: {key}, data: {b64_data}")

        return RetrieveDataResponse(b64_data=b64_data)

    @router.delete("/{key}")
    async def delete_data(key: str):
        logger.info(f"Deleting data, key: {key}")

        try:
            s3_service.delete_data(key)
        except KeyDoesNotExistError:
            logger.error(f"Failed to delete key: {key}, does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except StorageServiceError as e:
            logger.error(f"Failed to delete key: {key}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Deleted data for key: {key}")

    return router
