from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.workouts import create_workout, get_workout_by_id, get_all_workouts, update_workout, delete_workout
from app.schemas.workouts import WorkoutCreate, WorkoutResponse
from app.core.db import get_async_session
from app.models.users import User
from app.core.security import get_current_user

router = APIRouter(
    prefix='/workouts', 
    tags=['Тренировки 🏃‍♂️']
    )


@router.post(
        '/',
        tags=['Тренировки 🏃‍♂️'],
        summary='Создать новую тренировку',
        response_model=WorkoutResponse
        )
async def create_new_workout(
    workout_data: WorkoutCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Создание новой тренировки'''
    return await create_workout(session, workout_data, current_user.id)


@router.get(
        '/{workout_id}',
        tags=['Тренировки 🏃‍♂️'],
        summary='Получение тренировки по ID',
        response_model=WorkoutResponse
        )
async def get_workout(
    workout_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Получение тренировки по ID'''
    return await get_workout_by_id(session, workout_id)


@router.get(
        '/',
        tags=['Тренировки 🏃‍♂️'],
        summary='Получение всех тренировок',
        response_model=List[WorkoutResponse]
        )
async def get_user_workouts(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Получение всех тренировок текущего пользователя'''
    return await get_all_workouts(session, current_user.id)


@router.put(
        '/update/{workout_id}',
        tags=['Тренировки 🏃‍♂️'],
        summary='Обновление информации о тренировке',
        response_model=WorkoutResponse
        )
async def update_existing_workout(
    workout_id: int,
    workout_data: WorkoutCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Обновление информации о тренировке'''
    return await update_workout(session, workout_id, workout_data)


@router.delete(
        '/delete/{workout_id}',
        tags=['Тренировки 🏃‍♂️'],
        summary='Удаление тренировки',
        response_model=dict
        )
async def remove_workout(
    workout_id: int, 
    session: AsyncSession = Depends(get_async_session), 
    current_user: User = Depends(get_current_user)
    ):
    '''Удаление тренировки'''
    await delete_workout(session, workout_id)
    return {'message': 'Тренировка успешно удалена'}
