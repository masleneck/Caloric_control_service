from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.db import async_session_maker


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    '''
    Асинхронная сессия с автоматическим коммитом.
    get_session_with_commit создает сессию и автоматически выполняет коммит после завершения.
    Все изменения выполняются в одной транзакции.
    Если возникает ошибка, транзакция откатывается автоматически.
    '''
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    '''Асинхронная сессия без автоматического коммита(когда не меняем БД).'''
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
