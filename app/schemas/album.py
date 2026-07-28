from pydantic import BaseModel

from app.schemas.artista import ArtistaResponse
from app.schemas.genero import GeneroResponse


class AlbumResponse(BaseModel):
    id: int
    titulo: str
    artista: ArtistaResponse
    generos: list[GeneroResponse] = []
    class Config:
        from_attributes = True

class AlbumCreate(BaseModel):
    titulo: str
    artista_id: int
    genero_ids: list[int] = []