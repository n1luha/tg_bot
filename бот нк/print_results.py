import asyncio
from app.database.models import async_session, Result

async def print_all_results():
    async with async_session() as session:
        results = await session.execute(Result.__table__.select())
        for row in results.fetchall():
            print(f"{row.first_name} — {row.score} из {row.total}")

if __name__ == "__main__":
    asyncio.run(print_all_results())
