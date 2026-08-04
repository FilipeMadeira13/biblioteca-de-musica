from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreResponse


@app.post("/genres/", response_model=GenreResponse)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    genre_db = Genre(**genre.model_dump())
    db.add(genre_db)
    db.commit()
    db.refresh(genre_db)
    return genre_db


@app.get("/genres/", response_model=List[GenreResponse])
def list_genres(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    genres = db.query(Genre).offset(skip).limit(limit).all()
    return genres


@app.get("/genres/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found.")

    return genre


@app.put("/genres/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int, genre_updated: GenreCreate, db: Session = Depends(get_db)
):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found.")

    genre.name = genre_updated.name

    db.commit()
    db.refresh(genre)

    return genre


@app.delete("/genres/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()

    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found.")

    db.delete(genre)
    db.commit()
