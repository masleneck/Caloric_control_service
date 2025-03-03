from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.workouts import Workout
from app.schemas.workouts import WorkoutCreate, WorkoutUpdate



async def create_workout(session: AsyncSession, workout_data: WorkoutCreate, user_id: int) -> Workout:
    '''Создает тренировку'''
    workout = Workout(**workout_data.model_dump(), user_id=user_id)  
    session.add(workout)
    await session.commit()
    await session.refresh(workout)
    return workout    


async def get_workout_by_id(session: AsyncSession, workout_id: int) -> Optional[Workout]:
    '''Возвращает тренировку по ID'''
    workout = await session.get(Workout, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail='Тренировка не найдена')
    return workout


async def get_all_workouts(session: AsyncSession, user_id: int) -> List[Workout]:
    '''Получает список всех тренировок пользователя.'''
    result = await session.execute(select(Workout).filter(Workout.user_id == user_id))
    return result.scalars().all()


async def update_workout(session: AsyncSession, workout_id: int, workout_data: WorkoutUpdate) -> Optional[Workout]:
    '''Обновляет информацию о тренировке.'''
    result = await session.execute(select(Workout).filter(Workout.id == workout_id))
    workout = result.scalars().first()
    if not workout:
        raise HTTPException(status_code=404, detail='Тренировка не найдена')
    validated_workout = WorkoutUpdate.model_validate(workout_data) 
    for key, value in validated_workout.model_dump().items():
        setattr(workout, key, value)
    await session.commit()
    await session.refresh(workout)
    return workout


async def delete_workout(session: AsyncSession, workout_id: int) -> None:
    '''Удаляет тренировку по ID.'''
    result = await session.execute(select(Workout).filter(Workout.id == workout_id))
    workout = result.scalars().first()
    if not workout:
        raise HTTPException(status_code=404, detail='Тренировка не найдена')
    await session.delete(workout)
    await session.commit()
