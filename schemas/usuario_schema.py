from pydantic import BaseModel, EmailStr,ConfigDict
from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase(BaseModel):
    id: int | None = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    model_config = ConfigDict(from_attributes=True)
class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: list[ArtigoSchema] | None = None 

class UsuarioSchemaUp(BaseModel):
    nome: str | None = None
    sobrenome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
    eh_admin: bool | None = None

    model_config = ConfigDict(from_attributes=True)