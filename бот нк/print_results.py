import asyncio
from sqlalchemy import desc, asc
from app.database.models import async_session, Result

async def print_all_results():
    async with async_session() as session:
        query = Result.__table__.select().order_by(
            desc(Result.score),
            asc(Result.timestamp)
        )
        results = await session.execute(query)
        for row in results.fetchall():
            print(f"{row.first_name} — {row.score} из {row.total}")

if __name__ == "__main__":
    asyncio.run(print_all_results())
