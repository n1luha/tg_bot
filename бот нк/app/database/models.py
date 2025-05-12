from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Question(Base):
    __tablename__ = 'questions'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(255))
    option_1: Mapped[str] = mapped_column(String(100))
    option_2: Mapped[str] = mapped_column(String(100))
    option_3: Mapped[str] = mapped_column(String(100))
    correct_option: Mapped[int] = mapped_column(Integer)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)

class Result(Base):
    __tablename__ = 'results'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(100))
    score: Mapped[int] = mapped_column()
    total: Mapped[int] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
