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

@app.get('/artistas/', response_model=List[ArtistaCreate])
def listar_artistas(db: Session = Depends(get_db)):
    artistas = db.query(Artista).all()
    return artistas