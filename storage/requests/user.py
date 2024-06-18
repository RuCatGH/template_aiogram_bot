from sqlalchemy import select

from storage.models import User, async_session


async def get_user(session, tg_id: int) -> bool:
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    user = result.scalar()
    return user if user else None
