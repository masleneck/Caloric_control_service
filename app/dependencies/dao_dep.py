from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.db import async_session_maker


async def get_session():
    '''Генератор который отдает нам сессию пока ручка работает'''
    async with async_session_maker() as session: # создается новая асинхронная сессия
        yield session # генератор с сессией передается в вызывающую ф-цию

SessionDep = Annotated[AsyncSession, Depends(get_session)]


