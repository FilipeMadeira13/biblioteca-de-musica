from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    password: str = Field(min_length=8, max_length=72)
