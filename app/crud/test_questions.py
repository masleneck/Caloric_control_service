from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.test_questions import TestQuestion

async def get_test_questions(session: AsyncSession):
    '''Получить все вопросы из БД'''
    result = await session.execute(select(TestQuestion))
    return result.scalars().all()
