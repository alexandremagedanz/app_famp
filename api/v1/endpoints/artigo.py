from certifi import where
from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from core.deps import get_session, get_current_user 

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Cria um artigo", description="Essa rota cria um novo artigo no banco de dados.", response_model=ArtigoSchema, tags=["Artigos"])
async def post_artigo(artigo: ArtigoSchema, usuario_logaado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=str(artigo.url_fonte), usuario_id=usuario_logaado.id)
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ArtigoSchema], summary="Retorna todos os artigos", description="Essa rota retorna todos os artigos cadastrados no banco de dados.", tags=["Artigos"])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    query = select(ArtigoModel)
    result = await db.execute(query)
    artigos = result.scalars().unique().all()
    return artigos 

@router.get("/{artigo_id}", status_code=status.HTTP_200_OK, response_model=ArtigoSchema, summary="Retorna um artigo", description="Essa rota retorna um artigos cadastrado no banco de dados.", tags=["Artigos"])
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    query = select(ArtigoModel).where(ArtigoModel.id == artigo_id)
    result = await db.execute(query)
    artigo = result.scalar_one_or_none()
    if not artigo:
        raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
    return artigo

@router.put("/{artigo_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema, summary="Atualiza um artigo", description="Essa rota atualiza um artigo cadastrado no banco de dados.", tags=["Artigos"])
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logaado: UsuarioModel = Depends(get_current_user)):
    query = select(ArtigoModel).where(ArtigoModel.id == artigo_id)
    result = await db.execute(query)
    artigo_up = result.scalar_one_or_none()

    if not artigo_up:
        raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)
     
    if artigo.titulo:
        artigo_up.titulo = artigo.titulo
    if artigo.descricao:
        artigo_up.descricao = artigo.descricao
    if artigo.url_fonte:
        artigo_up.url_fonte = str(artigo.url_fonte)
    artigo_up.usuario_id = usuario_logaado.id
    await db.commit()
    return artigo_up
          
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT,  summary="Deleta um artigo", description="Essa rota deleta um artigo cadastrado no banco de dados.", tags=["Artigos"])
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logaado: UsuarioModel = Depends(get_current_user)):
    query = select(ArtigoModel).where(ArtigoModel.id == artigo_id).where(ArtigoModel.usuario_id == usuario_logaado.id)
    result = await db.execute(query)
    artigo_del = result.scalar_one_or_none()

    if not artigo_del:
        raise HTTPException(detail="Artigo nao encontrado", status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(artigo_del)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
