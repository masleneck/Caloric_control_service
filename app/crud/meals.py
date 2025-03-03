from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from typing import List
from datetime import datetime

from app.models.meals import Meal
from app.models.food_items import FoodItem
from app.schemas.meals import MealCreate, MealResponse, MealUpdate


def calculate_nutrients(food: FoodItem, quantity: float):
    '''Рассчитывает калории и БЖУ на основе веса продукта.'''
    factor = quantity / 100
    return {
        'calories': round(food.calories * factor, 2),
        'proteins': round(food.proteins * factor, 2),
        'fats': round(food.fats * factor, 2),
        'carbs': round(food.carbs * factor, 2),
    }


async def get_food_by_id(session: AsyncSession, food_id: int) -> FoodItem:
    '''Возвращает продукт по ID или вызывает 404-ошибку.'''
    result = await session.execute(select(FoodItem).filter(FoodItem.id == food_id))
    food = result.scalars().first()
    if not food:
        raise HTTPException(status_code=404, detail='Продукт не найден')
    return food


async def get_all_meals(session: AsyncSession, user_id: int) -> List[MealResponse]:
    '''Возвращает список всех приемов пищи пользователя.'''
    result = await session.execute(select(Meal).filter(Meal.user_id == user_id))
    meals = result.scalars().all()
    if not meals:
        return []
    # Получаем все food_id и загружаем продукты за один запрос
    food_ids = {meal.food_id for meal in meals}
    food_result = await session.execute(select(FoodItem).filter(FoodItem.id.in_(food_ids)))
    food_dict = {food.id: food for food in food_result.scalars().all()}
    # Формируем список ответов
    return [
        MealResponse(
            id=meal.id,
            food_id=meal.food_id,
            quantity=meal.quantity,
            datetime=meal.datetime,
            food_name=food_dict[meal.food_id].name,
            **calculate_nutrients(food_dict[meal.food_id], meal.quantity)
        )
        for meal in meals if meal.food_id in food_dict
    ]


async def create_meal(session: AsyncSession, meal_data: MealCreate, user_id: int) -> MealResponse:
    '''Добавляет новый прием пищи и рассчитывает БЖУ и калории.'''
    food = await get_food_by_id(session, meal_data.food_id)
    meal = Meal(
        user_id=user_id,
        food_id=meal_data.food_id,
        quantity=meal_data.quantity,
        datetime=datetime.utcnow()
    )
    session.add(meal)
    await session.commit()
    await session.refresh(meal)
    return MealResponse(
        id=meal.id,
        food_id=meal.food_id,
        quantity=meal.quantity,
        datetime=meal.datetime,
        food_name=food.name,
        **calculate_nutrients(food, meal.quantity)
    )


async def get_meal_by_id(session: AsyncSession, meal_id: int) -> MealResponse:
    '''Получает информацию о приеме пищи с расчетом калорий и БЖУ.'''
    result = await session.execute(select(Meal).filter(Meal.id == meal_id))
    meal = result.scalars().first()
    if not meal:
        raise HTTPException(status_code=404, detail='Прием пищи не найден')
    food = await get_food_by_id(session, meal.food_id)
    return MealResponse(
        id=meal.id,
        food_id=meal.food_id,
        quantity=meal.quantity,
        datetime=meal.datetime,
        food_name=food.name,
        **calculate_nutrients(food, meal.quantity)
    )


async def update_meal(session: AsyncSession, meal_id: int, meal_data: MealUpdate, user_id: int) -> MealResponse:
    '''Обновляет информацию о приеме пищи пользователя.'''
    result = await session.execute(select(Meal).filter(Meal.id == meal_id, Meal.user_id == user_id))
    meal = result.scalars().first()
    if not meal:
        raise HTTPException(status_code=404, detail='Прием пищи не найден или принадлежит другому пользователю')
    food = await get_food_by_id(session, meal_data.food_id)
    meal.food_id = meal_data.food_id
    meal.quantity = meal_data.quantity
    meal.datetime = meal_data.datetime or meal.datetime
    await session.commit()
    await session.refresh(meal)
    return MealResponse(
        id=meal.id,
        food_id=meal.food_id,
        quantity=meal.quantity,
        datetime=meal.datetime,
        food_name=food.name,
        **calculate_nutrients(food, meal.quantity)
    )


async def delete_meal(session: AsyncSession, meal_id: int) -> None:
    '''Удаляет прием пищи пользователя по ID.'''
    result = await session.execute(select(Meal).filter(Meal.id == meal_id))
    meal = result.scalars().first()
    if not meal:
        raise HTTPException(status_code=404, detail='Прием пищи не найден')
    await session.delete(meal)
    await session.commit()
