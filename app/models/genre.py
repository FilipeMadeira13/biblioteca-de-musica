from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.album import Album
from app.models.album_genre import album_genre


class Genre(Base):
    """
    Represents a music genre.

    Relationships:
        albums: list of albums associated with this genre (many-to-many via album_genre).
    """

    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))

    albums: Mapped[list["Album"]] = relationship(
        "Album", secondary=album_genre, back_populates="genres"
    )
