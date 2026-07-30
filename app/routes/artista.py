from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.main import app, get_db
from app.models.artista import Artista
from app.schemas.artista import ArtistaCreate, ArtistaResponse


@app.post("/artistas/", response_model=ArtistaResponse)
def criar_artista(artista: ArtistaCreate, db: Session = Depends(get_db)):
    artista_db = Artista(**artista.model_dump())
    db.add(artista_db)
    db.commit()
    db.refresh(artista_db)
    return artista_db


@app.get("/artistas/", response_model=List[ArtistaResponse])
def listar_artistas(db: Session = Depends(get_db)):
    artistas = db.query(Artista).all()
    return artistas


@app.get("/artistas/{artista_id}", response_model=ArtistaResponse)
def procurar_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado.")

    return artista


@app.put("/artistas/{artista_id}", response_model=ArtistaResponse)
def atualizar_artista(
    artista_id: int, artista_atualizado: ArtistaCreate, db: Session = Depends(get_db)
):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado.")

    artista.nome = artista_atualizado.nome
    artista.pais_origem = artista_atualizado.pais_origem
    artista.ano_formacao = artista_atualizado.ano_formacao

    db.commit()
    db.refresh(artista)

    return artista


@app.delete("/artistas/{artista_id}", status_code=204)
def excluir_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = db.query(Artista).filter(Artista.id == artista_id).first()

    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado.")

    db.delete(artista)
    db.commit()
