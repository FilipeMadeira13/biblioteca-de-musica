from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

album_genero = Table(
    'album_genero',
    Base.metadata,
    Column('album_id', Integer, ForeignKey('albuns.id'), primary_key=True),
    Column('genero_id', Integer, ForeignKey('generos.id'), primary_key=True)
)

class Artista(Base):
    """
    Representa um artista musical.

    Relacionamentos:
        albuns: lista de álbuns lançados pelo artista (um-para-muitos).
    """
    __tablename__ = 'artistas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    pais_origem: Mapped[str] = mapped_column(String(100))
    ano_formacao: Mapped[int] = mapped_column(Integer)

    albuns: Mapped[list['Album']] = relationship('Album', back_populates='artista')


class Genero(Base):
    """
    Representa um gênero musical.

    Relacionamentos:
        albuns: lista de álbuns associados a este gênero (muitos-para-muitos,
        via tabela associativa 'album_genero').
    """
    __tablename__ = 'generos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))

    albuns = relationship('Album', secondary=album_genero, back_populates='generos')

class Album(Base):
    """
    Representa um álbum musical.

    Relacionamentos:
        artista: artista responsável pelo álbum (muitos-para-um).
        generos: lista de gêneros associados a este álbum (muitos-para-muitos,
        via tabela associativa 'album_genero').
    """
    __tablename__ = 'albuns'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100))
    artista_id = Column(Integer, ForeignKey('artistas.id'))

    artista = relationship('Artista', back_populates='albuns')
    generos = relationship('Genero', secondary=album_genero, back_populates='albuns')

