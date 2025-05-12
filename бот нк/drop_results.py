import asyncio
from app.database.models import async_session, Result

async def drop_results_table():
    async with async_session() as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(Result.__table__.drop)
    print("✅ Таблица 'results' успешно удалена.")

if __name__ == "__main__":
    asyncio.run(drop_results_table())
