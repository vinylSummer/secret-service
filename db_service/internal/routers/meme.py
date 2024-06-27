import logging

from fastapi import APIRouter, status, HTTPException

from internal.routers.dto.meme import CreateMemeRequest, RetrieveMemeResponse, UpdateMemeRequest
from internal.database_service_interface import DatabaseServiceInterface
from internal.errors.errors import MemeDoesNotExistError, DBServiceError


logger = logging.getLogger(__name__)


def get_router(db_service: DatabaseServiceInterface):
    router = APIRouter(
        prefix="/memes"
    )

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_meme(request: CreateMemeRequest):
        # TODO: handle "meme already exists"
        meme = request.to_model()
        db_service.create_meme(meme)

    @router.get("/{meme_id}", response_model=RetrieveMemeResponse)
    async def retrieve_meme(meme_id: str) -> RetrieveMemeResponse:
        try:
            meme = db_service.retrieve_meme(meme_id)
        except MemeDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except DBServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        return RetrieveMemeResponse(
            meme_id=meme_id,
            image_id=meme.unique_image_id,
            caption=meme.caption
        )

    @router.get("/", response_model=list[RetrieveMemeResponse])
    async def retrieve_memes(skip: int = 0, limit: int = 3) -> list[RetrieveMemeResponse]:
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip parameter cannot be negative"
            )
        if limit < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit parameter cannot be negative"
            )

        logger.info(f"Retrieving memes at {skip=}, {limit=}")
        try:
            memes = db_service.retrieve_memes(skip, limit)
        except DBServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        if len(memes) == 0:
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

        logger.debug(f"Memes found:\n{response}")
        return response

    @router.put("/{meme_id}")
    async def update_meme(meme_id: str, request: UpdateMemeRequest):
        if request.image_id is None and request.caption is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data given for an update operation"
            )

        try:
            db_service.update_meme(meme_id, request.to_model(meme_id))
        except MemeDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except DBServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    @router.delete("/{meme_id}", response_model=RetrieveMemeResponse)
    async def delete_meme(meme_id: str) -> RetrieveMemeResponse:
        try:
            meme = db_service.delete_meme(meme_id)
        except MemeDoesNotExistError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except DBServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        return RetrieveMemeResponse(
            meme_id=meme_id,
            image_id=meme.unique_image_id,
            caption=meme.caption
        )

    return router
