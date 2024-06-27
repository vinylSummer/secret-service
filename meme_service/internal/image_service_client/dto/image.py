from pydantic import BaseModel


class CreateImageRequest(BaseModel):
    b64_data: str


class CreateImageResponse(BaseModel):
    image_id: str


class RetrieveImageRequest(BaseModel):
    image_id: str
    b64_data: str


class UpdateImageRequest(BaseModel):
    b64_data: str
