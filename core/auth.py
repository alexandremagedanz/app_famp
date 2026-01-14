from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import EmailStr

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha


TIMEZONE = ZoneInfo('America/Sao_Paulo')

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> UsuarioModel | None:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = await db.execute(query)
    usuario: UsuarioModel | None = result.scalar_one_or_none()

    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha):
        return None

    return usuario

def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    #https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4
    agora = datetime.now(TIMEZONE)
    expira =  agora + tempo_vida 
    payload = {
        'type': tipo_token,
        'exp': expira,
        'iat': agora,
        'sub': sub
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io
    """
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

