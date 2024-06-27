import logging

from fastapi import APIRouter, status, HTTPException

from internal.database_service_interface import DatabaseServiceInterface
from internal.errors.errors import MemeDoesNotExistError, ServiceError
from internal.routers.dto.meme import CreateMemeRequest, RetrieveMemeResponse, UpdateMemeRequest

logger = logging.getLogger(__name__)


def get_router(db_service: DatabaseServiceInterface):
    router = APIRouter(
        prefix="/memes"
    )

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_meme(request: CreateMemeRequest):
        logger.info(f"Creating meme {request}")
        # TODO: handle "meme already exists"
        try:
            db_service.create_meme(request.to_model())
        except ServiceError as e:
            logger.error(f"Could not create meme for request: {request}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Meme: {request} created successfully")

    @router.get("/{meme_id}", response_model=RetrieveMemeResponse)
    async def retrieve_meme(meme_id: str) -> RetrieveMemeResponse:
        logger.info(f"Retrieving meme: {meme_id}")

        try:
            meme = db_service.retrieve_meme(meme_id)
        except MemeDoesNotExistError:
            logger.error(f"Could not retrieve meme: {meme_id}, meme does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            logger.error(f"Could not retrieve meme: {meme_id}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        logger.info(f"Retrieved meme: {meme_id}")
        logger.debug(f"Retrieved meme: {meme}")

        return RetrieveMemeResponse(
            meme_id=meme_id,
            image_id=meme.unique_image_id,
            caption=meme.caption
        )

    @router.get("/", response_model=list[RetrieveMemeResponse])
    async def retrieve_memes(skip: int = 0, limit: int = 3) -> list[RetrieveMemeResponse]:
        logger.info(f"Retrieving memes at {skip=}, {limit=}")

        if skip < 0:
            logger.error(f"Can not retrieve memes at {skip=}, {limit=}, negative skip value")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip parameter cannot be negative"
            )
        if limit < 0:
            logger.error(f"Can not retrieve memes at {skip=}, {limit=}, negative limit value")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit parameter cannot be negative"
            )

        try:
            memes = db_service.retrieve_memes(skip, limit)
        except ServiceError as e:
            logger.error(f"Could not retrieve memes at {skip=}, {limit=}. Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        if len(memes) == 0:
            logger.error(f"Found no memes at {skip=}, {limit=}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )

        response: list[RetrieveMemeResponse] = []
        for meme in memes:
            r = RetrieveMemeResponse(
                meme_id=meme.unique_meme_id,
                image_id=meme.unique_image_id,
                caption=meme.caption
            )
            response.append(r)

        logger.info(f"Retrieved {len(response)} memes")
        logger.debug(f"Memes retrieved:\n{response}")

        return response

    @router.put("/{meme_id}")
    async def update_meme(meme_id: str, request: UpdateMemeRequest):
        logger.info(f"Updating meme: {meme_id}, update request: {request}")

        if request.image_id is None and request.caption is None:
            logger.error(f"Can not update meme: {meme_id}, no new data was provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data given for an update operation"
            )

        try:
            db_service.update_meme(meme_id, request.to_model(meme_id))
        except MemeDoesNotExistError:
            logger.error(f"Could not update meme: {meme_id}, meme does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            logger.error(f"Could not update meme: {meme_id}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Update meme: {meme_id}")

    @router.delete("/{meme_id}", response_model=RetrieveMemeResponse)
    async def delete_meme(meme_id: str) -> RetrieveMemeResponse:
        logger.info(f"Deleting meme: {meme_id}")

        try:
            meme = db_service.delete_meme(meme_id)
        except MemeDoesNotExistError:
            logger.error(f"Could not delete meme: {meme_id}, meme does not exist")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            logger.error(f"Could not delete meme: {meme_id}, error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Deleted meme: {meme_id}")

        return RetrieveMemeResponse(
            meme_id=meme_id,
            image_id=meme.unique_image_id,
            caption=meme.caption
        )

    return router
