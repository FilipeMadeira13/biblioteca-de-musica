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