from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.main import app
from app.models.album import Album
from app.models.artista import Artista
from app.models.genero import Genero
from app.schemas.album import AlbumCreate, AlbumResponse


@app.post("/albuns/", response_model=AlbumResponse)
def criar_album(album: AlbumCreate, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == album.artista_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado.")

    generos = db.query(Genero).filter(Genero.id.in_(album.genero_ids)).all()

    if len(generos) != len(album.genero_ids):
        raise HTTPException(
            status_code=404, detail="Um ou mais gêneros não foram encontrados."
        )

    album_db = Album(titulo=album.titulo, artista_id=album.artista_id, generos=generos)
    db.add(album_db)
    db.commit()
    db.refresh(album_db)
    return album_db


@app.get("/albuns/", response_model=List[AlbumResponse])
def listar_albuns(db: Session = Depends(get_db)):
    albuns = (
        db.query(Album)
        .options(joinedload(Album.artista), joinedload(Album.generos))
        .all()
    )
    return albuns


@app.get("/albuns/{album_id}", response_model=AlbumResponse)
def procurar_album(album_id: int, db: Session = Depends(get_db)):
    album = (
        db.query(Album)
        .options(joinedload(Album.artista), joinedload(Album.generos))
        .filter(Album.id == album_id)
        .first()
    )

    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado.")

    return album


@app.put("/albuns/{album_id}", response_model=AlbumResponse)
def atualizar_album(
    album_id: int, album_atualizado: AlbumCreate, db: Session = Depends(get_db)
):
    album = db.query(Album).filter(Album.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado.")

    artista = (
        db.query(Artista).filter(Artista.id == album_atualizado.artista_id).first()
    )

    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado.")

    generos = db.query(Genero).filter(Genero.id.in_(album_atualizado.genero_ids)).all()

    if len(generos) != len(album_atualizado.genero_ids):
        raise HTTPException(
            status_code=404, detail="Um ou mais gêneros não foram encontrados."
        )

    album.titulo = album_atualizado.titulo
    album.artista_id = album_atualizado.artista_id
    album.generos = generos

    db.commit()
    db.refresh(album)

    return album


@app.delete("/albuns/{album_id}", status_code=204)
def excluir_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado.")

    db.delete(album)
    db.commit()
