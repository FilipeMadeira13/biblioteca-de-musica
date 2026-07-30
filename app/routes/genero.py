from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.main import app
from app.models.genero import Genero
from app.schemas.genero import GeneroCreate, GeneroResponse


@app.post("/generos/", response_model=GeneroResponse)
def criar_genero(genero: GeneroCreate, db: Session = Depends(get_db)):
    genero_db = Genero(**genero.model_dump())
    db.add(genero_db)
    db.commit()
    db.refresh(genero_db)
    return genero_db


@app.get("/generos/", response_model=List[GeneroResponse])
def listar_generos(db: Session = Depends(get_db)):
    generos = db.query(Genero).all()
    return generos


@app.get("/generos/{genero_id}", response_model=GeneroResponse)
def procurar_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    return genero


@app.put("/generos/{genero_id}", response_model=GeneroResponse)
def atualizar_genero(
    genero_id: int, genero_atualizado: GeneroCreate, db: Session = Depends(get_db)
):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    genero.nome = genero_atualizado.nome

    db.commit()
    db.refresh(genero)

    return genero


@app.delete("/generos/{genero_id}", status_code=204)
def excluir_genero(genero_id: int, db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == genero_id).first()

    if not genero:
        raise HTTPException(status_code=404, detail="Gênero não encontrado.")

    db.delete(genero)
    db.commit()
