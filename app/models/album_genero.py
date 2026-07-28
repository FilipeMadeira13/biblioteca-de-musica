from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base


album_genero = Table(
    'album_genero',
    Base.metadata,
    Column('album_id', Integer, ForeignKey('albuns.id'), primary_key=True),
    Column('genero_id', Integer, ForeignKey('generos.id'), primary_key=True)
)