from pydantic import BaseModel

from app.schemas.artist import ArtistResponse
from app.schemas.genre import GenreResponse


class AlbumResponse(BaseModel):
    id: int
    title: str
    artist: ArtistResponse
    genres: list[GenreResponse] = []

    class Config:
        from_attributes = True


class AlbumCreate(BaseModel):
    title: str
    artist_id: int
    genre_ids: list[int] = []
