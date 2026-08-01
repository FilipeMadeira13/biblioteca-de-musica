from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.album import Album


class Artist(Base):
    """
    Represents a musical artist.

    Relationships:
        albums: list of albums released by the artist (one-to-many).
    """

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    country_of_origin: Mapped[str] = mapped_column(String(100))
    year_formed: Mapped[int] = mapped_column(Integer)

    albums: Mapped[list["Album"]] = relationship("Album", back_populates="artist")
