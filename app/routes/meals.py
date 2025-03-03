from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.meals import MealCreate, MealResponse, MealUpdate
from app.crud.meals import create_meal, get_meal_by_id, get_all_meals, update_meal, delete_meal
from app.core.security import get_current_user
from app.core.db import get_async_session
from app.models.users import User

router = APIRouter(
    prefix='/meals',
    tags=['Приемы пищи 🍽']
    )

@router.get(
        '/all',
        tags=['Приемы пищи 🍽'],
        summary='Получить список всех приемов пищи',
        response_model=List[MealResponse]
        )
async def get_all_meals_route(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю получить список всех своих приемов пищи'''
    return await get_all_meals(session, current_user.id)


@router.post(
        '/add',
        tags=['Приемы пищи 🍽'],
        summary='Добавить прием пищи',
        response_model=MealResponse
        )
async def add_meal(
    meal_data: MealCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю добавить прием пищи с автоматическим расчетом калорий, белков, жиров и углеводов'''
    return await create_meal(session, meal_data, current_user.id)


@router.get(
        '/get/{meal_id}',
        tags=['Приемы пищи 🍽'],
        summary='Получить прием пищи по ID',
        response_model=MealResponse
        )
async def get_meal(
    meal_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет пользователю получить информацию о приеме пищи с расчетом калорий, белков, жиров и углеводов'''
    return await get_meal_by_id(session, meal_id)


@router.put(
    '/update/{meal_id}',
    tags=['Приемы пищи 🍽'],
    summary='Обновить информацию о приеме пищи',
    response_model=MealResponse
)
async def update_meal_route(
    meal_id: int,
    meal_data: MealUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    '''Позволяет пользователю обновить свой прием пищи (изменить продукт, количество и время)'''
    return await update_meal(session, meal_id, meal_data, current_user.id)


@router.delete(
        '/delete/{meal_id}',
        tags=['Приемы пищи 🍽'],
        summary='Удалить прием пищи'
        )
async def remove_meal(
    meal_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    '''Удаляет прием пищи текущего пользователя.'''
    await delete_meal(session, meal_id)
    return {'message': f'Прием пищи с ID {meal_id} удален'}

