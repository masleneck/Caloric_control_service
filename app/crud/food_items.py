from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List, Optional

from app.models.food_items import FoodItem
from app.schemas.food_items import FoodCreate, FoodUpdate, FoodResponse


async def create_food(session: AsyncSession, food_data: FoodCreate) -> FoodItem:
    '''Создает новый продукт'''
    food = FoodItem(**food_data.model_dump())
    session.add(food)
    await session.commit()
    await session.refresh(food)
    return food


async def get_food_by_id(session: AsyncSession, food_id: int) -> Optional[FoodItem]:
    '''Возвращает продукт по ID'''
    food = await session.get(FoodItem, food_id)
    if not food:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    return food


async def get_all_foods(session: AsyncSession) -> List[FoodResponse]:
    '''Получает список всех продуктов'''
    result = await session.execute(select(FoodItem))
    foods = result.scalars().all()
    return [FoodResponse.model_validate(food) for food in foods]


async def update_food(session: AsyncSession, food_id: int, food_data: FoodUpdate) -> Optional[FoodItem]:
    '''Обновляет информацию о продукте(admin)'''
    result = await session.execute(select(FoodItem).filter(FoodItem.id == food_id))
    food = result.scalars().first()
    if not food:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    validated_food = FoodUpdate.model_validate(food_data) 
    for key, value in validated_food.model_dump().items():
        setattr(food, key, value)
    await session.commit()
    await session.refresh(food)
    return food


async def delete_food(session: AsyncSession, food_id: int) -> None:
    '''Удаляет продукт по ID(admin)'''
    result = await session.execute(select(FoodItem).filter(FoodItem.id == food_id))
    food = result.scalars().first()
    if not food:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    await session.delete(food)
    await session.commit()
