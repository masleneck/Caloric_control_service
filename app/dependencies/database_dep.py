from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker

async def get_async_session() -> AsyncSession:
    """Явное создание сессии без автокоммита"""
    return async_session_maker()