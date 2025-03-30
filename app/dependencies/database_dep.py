from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker

async def get_async_session():
    """Явное создание сессии без автокоммита"""
    async with async_session_maker() as session: # открывает сессию
        yield session  # передает сессию в обработчик запроса, а после завершения автоматически закрывает ее