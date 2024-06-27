from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Meme(Base):
    __tablename__ = "memes"

    # private id
    id = Column(Integer, primary_key=True)

    # public id
    unique_meme_id = Column(
        String,
        unique=True,
        index=True,
    )
    unique_image_id = Column(
        String,
        unique=True,
        index=True,
    )

    caption = Column(String, nullable=True)


class MemeUpdate(BaseModel):
    unique_meme_id: str | None
    unique_image_id: str | None
    caption: str | None
