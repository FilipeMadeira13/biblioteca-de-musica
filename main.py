from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal, engine
from models import Artista, Album, Genero, Base
from schemas import ArtistaResponse, ArtistaCreate, GeneroResponse, GeneroCreate, AlbumCreate, AlbumResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS - ARTISTA

@app.post('/artistas/', response_model=ArtistaResponse)
def criar_artista(artista: ArtistaCreate, db: Session = Depends(get_db)):
    artista_db = Artista(**artista.model_dump())
    db.add(artista_db)
    db.commit()
    db.refresh(artista_db)
    return artista_db

@app.get('/artistas/', response_model=List[ArtistaResponse])
def listar_artistas(db: Session = Depends(get_db)):
    artistas = db.query(Artista).all()
    return artistas

@app.get('/artistas/{artista_id}', response_model=ArtistaResponse)
def procurar_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail='Artista não encontrado.')

    return artista

@app.put('/artistas/{artista_id}', response_model=ArtistaResponse)
def atualizar_artista(artista_id: int, artista_atualizado: ArtistaCreate, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail='Artista não encontrado.')

    artista.nome = artista_atualizado.nome
    artista.pais_origem = artista_atualizado.pais_origem
    artista.ano_formacao = artista_atualizado.ano_formacao

    db.commit()
    db.refresh(artista)

    return artista

@app.delete('/artistas/{artista_id}', status_code=204)
def excluir_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail='Artista não encontrado.')

    db.delete(artista)
    db.commit()

# ENDPOINTS - GENERO

@app.post('/generos/', response_model=GeneroResponse)
def criar_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    genero_db = Genero(**genero.model_dump())
    db.add(genero_db)
    db.commit()
    db.refresh(genero_db)
    return genero_db

@app.get('/generos/', response_model=List[GeneroResponse])
def listar_generos(db: Session = Depends(get_db)):
    generos = db.query(Genero).all()
    return generos

@app.get('/generos/{genero_id}', response_model=GeneroResponse)
def procurar_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not genero:
        raise HTTPException(status_code=404, detail='Gênero não encontrado.')

    return genero

@app.put('/generos/{genero_id}', response_model=GeneroResponse)
def atualizar_genero(genero_id: int, genero_atualizado: GeneroCreate, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not genero:
        raise HTTPException(status_code=404, detail='Gênero não encontrado.')

    genero.nome = genero_atualizado.nome

    db.commit()
    db.refresh(genero)

    return genero

@app.delete('/generos/{genero_id}', status_code=204)
def excluir_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()
    
    if not genero:
        raise HTTPException(status_code=404, detail='Gênero não encontrado.')

    db.delete(genero)
    db.commit()

# ENDPOINTS - ALBUM

@app.post('/albuns/', response_model=AlbumResponse)
def criar_album(album: AlbumCreate, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == album.artista_id).first()
    if not artista:
        raise HTTPException(status_code=404, detail='Artista não encontrado.')

    generos = db.query(Genero).filter(Genero.id.in_(album.genero_ids)).all()

    if len(generos) != len(album.genero_ids):
        raise HTTPException(status_code=404, detail='Um ou mais gêneros não foram encontrados.')

    album_db = Album(
        titulo=album.titulo,
        artista_id=album.artista_id,
        generos=generos
    )
    db.add(album_db)
    db.commit()
    db.refresh(album_db)
    return album_db

@app.get('/albuns/', response_model=List[AlbumResponse])
def listar_albuns(db: Session = Depends(get_db)):
    albuns = db.query(Album).options(joinedload(Album.artista), joinedload(Album.generos)).all()
    return albuns

@app.get('/albuns/{album_id}', response_model=AlbumResponse)
def procurar_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).options(joinedload(Album.artista), joinedload(Album.generos)).filter(Album.id == album_id).first()

    if not album:
        raise HTTPException(status_code=404, detail='Álbum não encontrado.')

    return album

@app.put('/albuns/{album_id}', response_model=AlbumResponse)
def atualizar_album(album_id: int, album_atualizado: AlbumCreate, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    
    if not album:
        raise HTTPException(status_code=404, detail='Álbum não encontrado.')

    artista = db.query(Artista).filter(Artista.id == album_atualizado.artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail='Artista não encontrado.')

    generos = db.query(Genero).filter(Genero.id.in_(album_atualizado.genero_ids)).all()
    
    if len(generos) != len(album_atualizado.genero_ids):
        raise HTTPException(status_code=404, detail='Um ou mais gêneros não foram encontrados.')
    
    album.titulo = album_atualizado.titulo
    album.artista_id = album_atualizado.artista_id
    album.genero_ids = generos
    
    db.commit()
    db.refresh(album)

    return album