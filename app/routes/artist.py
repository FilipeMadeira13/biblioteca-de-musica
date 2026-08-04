from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app
from app.models.artist import Artist
from app.schemas.artist import ArtistCreate, ArtistResponse


@app.post("/artists/", response_model=ArtistResponse)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    artist_db = Artist(**artist.model_dump())
    db.add(artist_db)
    db.commit()
    db.refresh(artist_db)
    return artist_db


@app.get("/artists/", response_model=List[ArtistResponse])
def list_artists(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    artists = db.query(Artist).offset(skip).limit(limit).all()
    return artists


@app.get("/artists/{artist_id}", response_model=ArtistResponse)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found.")

    return artist


@app.put("/artists/{artist_id}", response_model=ArtistResponse)
def update_artist(
    artist_id: int, artist_updated: ArtistCreate, db: Session = Depends(get_db)
):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found.")

    artist.name = artist_updated.name
    artist.country_of_origin = artist_updated.country_of_origin
    artist.year_formed = artist_updated.year_formed

    db.commit()
    db.refresh(artist)

    return artist


@app.delete("/artists/{artist_id}", status_code=204)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == artist_id).first()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found.")

    db.delete(artist)
    db.commit()
