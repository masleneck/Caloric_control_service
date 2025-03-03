from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.users import User
from app.schemas.food_items import FoodCreate, FoodResponse
from app.crud.food_items import create_food, get_food_by_id, get_all_foods, update_food, delete_food
from app.core.security import get_current_user, is_admin
from app.core.db import get_async_session

router = APIRouter(
    prefix='/food',
    tags=['Продукты питания 🍏']
    )


@router.post(
        '/add',
        tags=['Продукты питания 🍏'],
        summary='Добавить новый продукт',
        response_model=FoodResponse
        )
async def add_food(
    food_data: FoodCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет любому пользователю добавить продукт в базу'''
    return await create_food(session, food_data)


@router.get(
        '/get/{food_id}',
        tags=['Продукты питания 🍏'],
        summary='Получить продукт по ID',
        response_model=FoodResponse
        )
async def get_food(
    food_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет любому пользователю получить информацию о продукте'''
    return await get_food_by_id(session, food_id)


@router.get(
        '/list',
        tags=['Продукты питания 🍏'],
        summary='Получить список всех продуктов',
        response_model=List[FoodResponse]
        )
async def get_food_list(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
    ):
    '''Позволяет любому пользователю получить список всех продуктов'''
    return await get_all_foods(session)


@router.put(
        '/update/{food_id}',
        tags=['Продукты питания 🍏'],
        summary='🟢 Обновить информацию о продукте',
        response_model=FoodResponse
        )
async def update_food_info(
    food_id: int,
    food_data: FoodCreate,
    session: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(is_admin)  
    ):
    '''Позволяет администратору обновить информацию о продукте'''
    return await update_food(session, food_id, food_data)


@router.delete(
        '/delete/{food_id}',
        tags=['Продукты питания 🍏'],
        summary='🟢 Удалить продукт'
        )
async def delete_food_item(
    food_id: int,
    session: AsyncSession = Depends(get_async_session),
    admin_user: User = Depends(is_admin)
    ):
    '''Позволяет администратору удалить продукт'''
    await delete_food(session, food_id)
    return {'message': f'Продукт с ID {food_id} удален'}
