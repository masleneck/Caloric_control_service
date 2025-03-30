from sqlalchemy import select
from typing import List
from app.repositories.base import BaseDAO
from app.models import TestQuestion

class QuestionDAO(BaseDAO[TestQuestion]):
    model = TestQuestion

    async def find_all(self) -> List[TestQuestion]:
        '''Возвращает все вопросы, отсортированные по ID'''
        query = select(self.model).order_by(self.model.id)  # Сортировка по ID
        result = await self._session.execute(query)
        return result.scalars().all()