from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.album_genre import album_genre

if TYPE_CHECKING:
    from app.models.artist import Artist
    from app.models.genre import Genre


class Album(Base):
    """
    Represents a music album.

    Relationships:
        artist: the album's artist (many-to-one).
        genres: genres linked to the album (many-to-many via album_genre).
    """

    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    artist_id: Mapped[int] = mapped_column(Integer, ForeignKey("artists.id"))

    artist: Mapped["Artist"] = relationship("Artist", back_populates="albums")
    genres: Mapped[list["Genre"]] = relationship(
        "Genre", secondary=album_genre, back_populates="albums"
    )
