from typing import List
import uuid
from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database_dep import get_async_session
from app.repositories.questons import QuestionDAO
from app.schemas.test_questions import TestQuestionResponse, MetricsRequest  # Импортируем схему
from app.models import TestResult
from app.core.calculations import calculate_metrics


router = APIRouter(prefix='/questions', tags=['Вопросы ❓️'])


@router.get('/', response_model=List[TestQuestionResponse], summary='Получить все вопросы')
async def get_questions(
    session: AsyncSession = Depends(get_async_session),
) -> List[TestQuestionResponse]:
    '''Возвращает список всех вопросов для опросника, отсортированных по ID'''
    return await QuestionDAO(session).find_all()


@router.post('/calculate', summary='Результат теста')
async def calculate_metrics_api(data: MetricsRequest):
    '''Эндпоинт для расчёта метрик'''
    return calculate_metrics(data.model_dump())  # Преобразуем в словарь


@router.post('/save_test_result', summary='Сохранить результаты теста')
async def save_test_result(
    data: MetricsRequest,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
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
    # Устанавливаем куку с session_id
    response.set_cookie(key='session_id', value=session_id, httponly=True)
    return {'session_id': session_id}