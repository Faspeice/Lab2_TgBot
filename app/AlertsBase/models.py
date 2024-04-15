from sqlalchemy import  BigInteger, String, ForeignKey
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


class Alert(Base):
    __tablename__ = 'alerts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    cost: Mapped[str] = mapped_column(String(25))
    procent: Mapped[str] = mapped_column(String(25))
    val1: Mapped[str] = mapped_column(String(25))
    val2: Mapped[str] = mapped_column(String(25))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
