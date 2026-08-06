from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI()

from app.routers import album, artist, genre, user, auth

Base.metadata.create_all(bind=engine)
