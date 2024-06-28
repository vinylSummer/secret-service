from pydantic import BaseModel


class CreateDataRequest(BaseModel):
    key: str
    b64_data: str


class RetrieveDataResponse(BaseModel):
    b64_data: str
