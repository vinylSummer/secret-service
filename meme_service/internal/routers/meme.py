import logging

from fastapi import status, APIRouter, HTTPException

from internal.errors.errors import MemeNotFoundError, ServiceError
from internal.routers.dto.meme import RetrieveMemeResponse, CreateMemeRequest, UpdateMemeRequest, CreateMemeResponse
from internal.meme_service_interface import MemeServiceInterface


logger = logging.getLogger(__name__)


def get_router(meme_service: MemeServiceInterface) -> APIRouter:
    router = APIRouter(
        prefix="/memes",
        tags=["memes"],
    )

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateMemeResponse)
    async def create_meme(request: CreateMemeRequest):
        logger.info(f"Creating meme: {request}")

        meme = request.to_model()
        try:
            meme_service.create_meme(meme)
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Successfully created meme: {meme}")

        return CreateMemeResponse(
            meme_id=meme.id
        )

    @router.get("/{meme_id}", response_model=RetrieveMemeResponse)
    async def retrieve_meme(meme_id: str) -> RetrieveMemeResponse:
        logger.info(f"Retrieving meme with id: {meme_id}")

        try:
            meme = meme_service.retrieve_meme(meme_id)
        except MemeNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        logger.info(f"Successfully retrieved meme: {meme} for meme id: {meme_id}")

        return RetrieveMemeResponse(
            b64_data=meme.b64_data,
            caption=meme.caption
        )

    @router.get("/", response_model=list[RetrieveMemeResponse])
    async def retrieve_memes(skip: int = 0, limit: int = 3) -> list[RetrieveMemeResponse]:
        logger.info(f"Retrieving memes at {skip=}, {limit=}")

        try:
            memes = meme_service.retrieve_memes(skip, limit)
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        response: list[RetrieveMemeResponse] = []
        for meme in memes:
            r = RetrieveMemeResponse(
                b64_data=meme.b64_data,
                caption=meme.caption
            )
            response.append(r)

        logger.info(f"Successfully retrieved {len(response)} memes for {skip=}, {limit=}: {response}")
        return response

    @router.put("/{meme_id}")
    async def update_meme(meme_id: str, request: UpdateMemeRequest):
        logger.info(f"Updating meme with id: {meme_id}, update request: {request}")
        if request.b64_data is None and request.caption is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No new data given for an update operation"
            )
        try:
            meme_service.update_meme(meme_id, request.to_model(meme_id))
        except MemeNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        logger.info(f"Successfully updated meme with id: {meme_id}")

    @router.delete("/{meme_id}")
    async def delete_meme(meme_id: str):
        logger.info(f"Deleting meme with id: {meme_id}")
        try:
            meme_service.delete_meme(meme_id)
        except MemeNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        logger.info(f"Successfully deleted meme with id: {meme_id}")

    return router
