from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

album_genre = Table(
    "album_genre",
    Base.metadata,
    Column("album_id", Integer, ForeignKey("albums.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)
