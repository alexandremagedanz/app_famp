from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.configs import DBBaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.usuario_model import UsuarioModel
class ArtigoModel(DBBaseModel):
    __tablename__ = "artigos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(256))
    descricao: Mapped[str] = mapped_column(String(256))
    url_fonte: Mapped[str] = mapped_column(String(256))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    criador: Mapped["UsuarioModel"] = relationship("UsuarioModel", back_populates="artigos", lazy="joined")