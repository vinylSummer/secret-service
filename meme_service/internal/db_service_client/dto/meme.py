from pydantic import BaseModel


class CreateMemeRequest(BaseModel):
    meme_id: str
    image_id: str
    caption: str | None


class RetrieveMemeResponse(BaseModel):
    meme_id: str
    image_id: str
    caption: str | None

