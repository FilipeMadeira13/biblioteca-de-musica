from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    nome: str
    senha: str = Field(min_length=8)
