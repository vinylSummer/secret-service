import uuid

from pydantic import BaseModel, Field


class Image(BaseModel):
    image_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    b64_data: str

