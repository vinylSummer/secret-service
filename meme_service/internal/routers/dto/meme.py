from pydantic import BaseModel

from models.meme import Meme


class CreateMemeRequest(BaseModel):
    b64_data: str
    caption: str | None = None

    def to_model(self) -> Meme:
        return Meme(
            b64_data=self.b64_data,
            caption=self.caption
        )


class CreateMemeResponse(BaseModel):
    meme_id: str


class RetrieveMemeResponse(BaseModel):
    b64_data: str
    caption: str | None = None


class UpdateMemeRequest(BaseModel):
    b64_data: str | None = None
    caption: str | None = None

    def to_model(self, meme_id: str) -> Meme:
        if self.b64_data is None:
            self.b64_data = ""
        return Meme(
            id=meme_id,
            b64_data=self.b64_data,
            caption=self.caption
        )
