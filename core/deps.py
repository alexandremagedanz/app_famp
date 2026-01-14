from re import A
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.databese import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel

class TokenData(BaseModel):
    username: str | None = None

async def get_section() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_schema), db: AsyncSession  = Depends(get_section)) -> UsuarioModel:
    exception_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possivel validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
            )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise exception_credentials
        token_data = TokenData(username=user_id)
    except JWTError:
        raise exception_credentials

    try:
        user_id_val = int(token_data.username) if token_data.username is not None else None
        if user_id_val is None:
            raise exception_credentials
        user_id_int = user_id_val
    except ValueError:
        raise exception_credentials

    query = select(UsuarioModel).where(UsuarioModel.id == user_id_int)
    result = await db.execute(query)
    usuario = result.scalars().unique().one_or_none()
    if usuario is None:
        raise exception_credentials
    return usuario