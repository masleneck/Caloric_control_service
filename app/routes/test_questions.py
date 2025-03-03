from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from app.crud.test_questions import get_test_questions
from app.schemas.test_questions import TestQuestionResponse
from app.core.db import get_async_session

router = APIRouter()

@router.get('/test', response_model=List[TestQuestionResponse])
async def get_test(session: AsyncSession = Depends(get_async_session)):
    '''Получить список вопросов для теста'''
    return await get_test_questions(session)
