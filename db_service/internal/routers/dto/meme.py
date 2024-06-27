from pydantic import BaseModel

from models.meme import Meme


class CreateMemeRequest(BaseModel):
    meme_id: str
    image_id: str
    caption: str | None = None

    def to_model(self):
        return Meme(
            unique_meme_id=self.meme_id,
            unique_image_id=self.image_id,
            caption=self.caption,
        )


# class CreateMemeResponse(BaseModel):
#     pass


# class RetrieveMemeRequest(BaseModel):
#     pass


class RetrieveMemeResponse(BaseModel):
    meme_id: str
    image_id: str
    caption: str | None = None


class UpdateMemeRequest(BaseModel):
    meme_id: str | None = None
    image_id: str | None = None
    caption: str | None = None

    def to_model(self, meme_id: str):
        return Meme(
            unique_meme_id=meme_id,
            unique_image_id=self.image_id,
            caption=self.caption,
        )

# class UpdateMemeResponse(BaseModel):
#     pass


# class DeleteMemeRequest(BaseModel):
#     pass


# class DeleteMemeResponse(BaseModel):
#     pass
