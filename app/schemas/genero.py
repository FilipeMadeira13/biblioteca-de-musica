from pydantic import BaseModel


class GeneroResponse(BaseModel):
    id: int
    nome: str
    class Config:
        from_attributes = True

class GeneroCreate(BaseModel):
    nome: str