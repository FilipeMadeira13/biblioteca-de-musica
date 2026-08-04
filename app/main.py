from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI()

from app.routes import album, artist, genre, user

Base.metadata.create_all(bind=engine)
