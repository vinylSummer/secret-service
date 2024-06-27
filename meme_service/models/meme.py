import uuid

from pydantic import BaseModel, Field


class Meme(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    b64_data: str
    caption: str | None

    # def __eq__(self, other):
    #     return (self.id == other.id and
    #             self.b64_data == other.b64_data and
    #             self.caption == other.caption
    #             )


class DBMeme(BaseModel):
    id: str
    image_id: str
    caption: str | None
