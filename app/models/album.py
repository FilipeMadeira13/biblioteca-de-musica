from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.album_genero import album_genero
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.artista import Artista
    from app.models.genero import Genero

class Album(Base):
    """
    Representa um álbum musical.

    Relacionamentos:
        artista: artista responsável pelo álbum (muitos-para-um).
        generos: lista de gêneros associados a este álbum (muitos-para-muitos,
        via tabela associativa 'album_genero').
    """
    __tablename__ = 'albuns'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(100))
    artista_id: Mapped[int] = mapped_column(Integer, ForeignKey('artistas.id'))

    artista: Mapped['Artista'] = relationship('Artista', back_populates='albuns')
    generos: Mapped[list['Genero']] = relationship('Genero', secondary=album_genero, back_populates='albuns')