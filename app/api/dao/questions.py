from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dao.base import BaseDAO
from app.models.test_questions import TestQuestion

class QuestionDAO(BaseDAO[TestQuestion]):
    model = TestQuestion

    async def find_all(self) -> List[TestQuestion]:
        '''Возвращает все вопросы, отсортированные по ID'''
        query = select(self.model).order_by(self.model.id)  # Сортировка по ID
        result = await self._session.execute(query)
        return result.scalars().all()