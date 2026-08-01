from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI()

from app.routes import album, artist, genre

Base.metadata.create_all(bind=engine)
