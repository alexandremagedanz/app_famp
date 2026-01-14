import asyncio
from core.configs import DBBaseModel
from core.databese import engine

async def create_tables() -> None:
    import models.__all_models
    print("Conectando ao banco de dados...")
    print("Criando as tabelas...")

    async with engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)
        await conn.run_sync(DBBaseModel.metadata.create_all)
    print("Sucesso: Tabelas 'usuarios' e 'artigos' criadas!")

if __name__ == "__main__":
    asyncio.run(create_tables()) 