from pydantic import BaseModel


class ArtistResponse(BaseModel):
    id: int
    name: str
    country_of_origin: str
    year_formed: int

    class Config:
        from_attributes = True


class ArtistCreate(BaseModel):
    name: str
    country_of_origin: str
    year_formed: int
