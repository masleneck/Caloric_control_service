from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.dao_dep import get_session_without_commit
from app.data.dao import QuestionDAO
from app.schemas.test_questions import TestQuestionResponse  # Импортируем схему

router = APIRouter(prefix='/questions', tags=['Вопросы ❓️'])


@router.get('/', response_model=List[TestQuestionResponse], summary='Получить все вопросы')
async def get_questions(
    session: AsyncSession = Depends(get_session_without_commit),
) -> List[TestQuestionResponse]:
    '''Возвращает список всех вопросов для опросника, отсортированных по ID'''
    questions = await QuestionDAO(session).find_all()
    return questions