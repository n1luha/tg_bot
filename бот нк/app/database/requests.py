from sqlalchemy import select, desc
from app.database.models import async_session
from app.database.models import User, Question, Result

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_all_questions():
    async with async_session() as session:
        result = await session.scalars(select(Question))
        return list(result)

async def save_result(tg_id, first_name, score, total):
    async with async_session() as session:
        session.add(Result(
            tg_id=tg_id,
            first_name=first_name,
            score=score,
            total=total
        ))
        await session.commit()

async def get_top_results(limit: int = 3):
    async with async_session() as session:
        result = await session.execute(
            select(Result).order_by(desc(Result.score)).limit(limit)
        )
        return result.scalars().all()

async def has_played(tg_id: int) -> bool:
    async with async_session() as session:
        result = await session.scalar(
            select(Result).where(Result.tg_id == tg_id)
        )
        return result is not None
