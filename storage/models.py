import asyncio

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, as_declarative
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import USER_DB, PASSWORD_DB, DB_NAME

engine = create_async_engine(
    f"postgresql+asyncpg://{USER_DB}:{PASSWORD_DB}@localhost/{DB_NAME}", echo=False)

async_session = async_sessionmaker(engine)


@as_declarative()
class AbstractModel:
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True)


class User(AbstractModel):
    __tablename__ = "users"

    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(AbstractModel.metadata.create_all)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(start_db())
    loop.close()
