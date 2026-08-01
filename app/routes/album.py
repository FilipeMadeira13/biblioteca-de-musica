from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.main import app
from app.models.album import Album
from app.models.artist import Artist
from app.models.genre import Genre
from app.schemas.album import AlbumCreate, AlbumResponse


@app.post("/albums/", response_model=AlbumResponse)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found.")

    genres = db.query(Genre).filter(Genre.id.in_(album.genre_ids)).all()

    if len(genres) != len(album.genre_ids):
        raise HTTPException(
            status_code=404, detail="One or more genres were not found."
        )

    album_db = Album(title=album.title, artist_id=album.artist_id, genres=genres)
    db.add(album_db)
    db.commit()
    db.refresh(album_db)
    return album_db


@app.get("/albums/", response_model=List[AlbumResponse])
def list_albums(db: Session = Depends(get_db)):
    albums = (
        db.query(Album)
        .options(joinedload(Album.artist), joinedload(Album.genres))
        .all()
    )
    return albums


@app.get("/albums/{album_id}", response_model=AlbumResponse)
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = (
        db.query(Album)
        .options(joinedload(Album.artist), joinedload(Album.genres))
        .filter(Album.id == album_id)
        .first()
    )

    if not album:
        raise HTTPException(status_code=404, detail="Album not found.")

    return album


@app.put("/albums/{album_id}", response_model=AlbumResponse)
def update_album(
    album_id: int, album_updated: AlbumCreate, db: Session = Depends(get_db)
):
    album = db.query(Album).filter(Album.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail="Album not found.")

    artist = db.query(Artist).filter(Artist.id == album_updated.artist_id).first()

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found.")

    genres = db.query(Genre).filter(Genre.id.in_(album_updated.genre_ids)).all()

    if len(genres) != len(album_updated.genre_ids):
        raise HTTPException(
            status_code=404, detail="One or more genres were not found."
        )

    album.title = album_updated.title
    album.artist_id = album_updated.artist_id
    album.genres = genres

    db.commit()
    db.refresh(album)

    return album


@app.delete("/albums/{album_id}", status_code=204)
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail="Album not found.")

    db.delete(album)
    db.commit()
