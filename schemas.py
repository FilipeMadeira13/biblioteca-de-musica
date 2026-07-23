from pydantic import BaseModel

class ArtistaResponse(BaseModel):
    id: int
    nome: str
    pais_origem: str
    ano_formacao: int
    class Config:
        from_attributes = True

class ArtistaCreate(BaseModel):
    nome: str
    pais_origem: str
    ano_formacao: int

class GeneroResponse(BaseModel):
    id: int
    nome: str
    class Config:
        from_attributes = True

class GeneroCreate(BaseModel):
    nome: str

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