from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.album_genero import album_genero
from app.models.album import Album
from database import Base


class Genero(Base):
    """
    Representa um gênero musical.

    Relacionamentos:
        albuns: lista de álbuns associados a este gênero (muitos-para-muitos,
        via tabela associativa 'album_genero').
    """
    __tablename__ = 'generos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))

    albuns: Mapped[list['Album']] = relationship('Album', secondary=album_genero, back_populates='generos')