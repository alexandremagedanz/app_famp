from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.configs import DBBaseModel

if TYPE_CHECKING:
    from models.artigo_model import ArtigoModel
class UsuarioModel(DBBaseModel):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(256), nullable=True)
    sobrenome: Mapped[str] = mapped_column(String(256), nullable=True)
    email: Mapped[str] = mapped_column(String(256), index=True, unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(256), nullable=False)
    eh_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    artigos: Mapped[List["ArtigoModel"]] = relationship("ArtigoModel", cascade="all, delete-orphan", back_populates="criador", uselist=True, lazy="joined")
