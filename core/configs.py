from pyexpat import model
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    #Configurações gerais da aplicação
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cursos API - Segurança e Autenticação"

    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_NAME: str = ""

    API_JWT_SECRET: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    """
    Gerendo um Secret Key para JWT - rodar no python shell
    import secrets
    secrets.token_urlsafe(32)
    """

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def JWT_SECRET(self) -> str:
        return self.API_JWT_SECRET

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive = True
    )

settings = Settings()

class DBBaseModel(DeclarativeBase):
    pass