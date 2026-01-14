from pydantic import BaseModel, HttpUrl, ConfigDict

class ArtigoSchema(BaseModel):
    id: int | None = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: int | None = None

    model_config = ConfigDict(from_attributes=True)