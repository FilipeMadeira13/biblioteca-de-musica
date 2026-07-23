from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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
def listar_artista(artista_id: int, db: Session = Depends(get_db)):
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