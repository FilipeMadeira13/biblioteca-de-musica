from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.album import Album


class Artista(Base):
    """
    Representa um artista musical.

    Relacionamentos:
        albuns: lista de álbuns lançados pelo artista (um-para-muitos).
    """

    __tablename__ = "artistas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    pais_origem: Mapped[str] = mapped_column(String(100))
    ano_formacao: Mapped[int] = mapped_column(Integer)

    albuns: Mapped[list["Album"]] = relationship("Album", back_populates="artista")
