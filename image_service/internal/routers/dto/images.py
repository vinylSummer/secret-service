from pydantic import BaseModel

from models.image import Image


class CreateImageRequest(BaseModel):
    b64_data: str

    def to_model(self) -> Image:
        return Image(
            b64_data=self.b64_data
        )


class CreateImageResponse(BaseModel):
    image_id: str


# class GetImageRequest(BaseModel):
#     pass


class GetImageResponse(BaseModel):
    b64_data: str


class UpdateImageRequest(BaseModel):
    b64_data: str

    def to_model(self, image_id: str) -> Image:
        return Image(
            image_id=image_id,
            b64_data=self.b64_data
        )


class UpdateImageResponse(BaseModel):
    pass


# class DeleteImageRequest(BaseModel):
#     pass


class DeleteImageResponse(BaseModel):
    pass
