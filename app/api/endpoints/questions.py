from typing import List
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.dao_dep import get_session_without_commit, get_session_with_commit
from app.data.dao import QuestionDAO
from app.schemas.test_questions import TestQuestionResponse, MetricsRequest  # Импортируем схему
from app.models import TestResult
from app.core.calculations import calculate_metrics


router = APIRouter(prefix='/questions', tags=['Вопросы ❓️'])


@router.get('/', response_model=List[TestQuestionResponse], summary='Получить все вопросы')
async def get_questions(
    session: AsyncSession = Depends(get_session_without_commit),
) -> List[TestQuestionResponse]:
    '''Возвращает список всех вопросов для опросника, отсортированных по ID'''
    questions = await QuestionDAO(session).find_all()
    return questions


@router.post('/calculate', summary='Результат теста')
async def calculate_metrics_api(data: MetricsRequest):
    '''Эндпоинт для расчёта метрик'''
    result = calculate_metrics(data.model_dump())  # Преобразуем в словарь
    return result


@router.post('/save_test_result/', summary='Сохранить результаты теста')
async def save_test_result(
    data: MetricsRequest,
    session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    '''Сохранить результаты теста для неавторизованного пользователя.'''
    session_id = str(uuid.uuid4())  # Генерируем уникальный session_id
    test_result = TestResult(
        session_id=session_id,
        gender=data.gender,
        birthday_date=data.birthday_date,
        height=data.height,
        weight=data.weight,
        goal=data.goal,
    )
    session.add(test_result)
    await session.commit()
    return {'session_id': session_id}