from datetime import date
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.repositories.food_item import FoodItemDAO
from app.repositories.meal import MealDAO
from app.dependencies.database_dep import get_async_session
from app.dependencies.auth_dep import get_current_admin_user, get_current_user
from app.schemas.meals import DailyMealsResponse, DailyNutritionResponse, FoodItemCreate, FoodItemResponse, MealResponse, MealUpsertRequest

router = APIRouter(
   prefix='/meals',
   tags=['Приёмы пищи 🍽']
)

@router.post("/upsert_meal", response_model=MealResponse, summary="Обновить/Создать прием пищи")
async def upsert_meal(
    meal_data: MealUpsertRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    meal = await MealDAO(session).upsert_meal_with_items(user.id, meal_data)
    # Формируем ответ с продуктами
    food_items = [
        {"name": name, "quantity": qty}
        for name, qty in zip(meal_data.food_names, meal_data.food_quantities)
    ]
    return {
        "id": meal.id,
        "mealtime": meal.mealtime,
        "meal_date": meal.meal_date,
        "food_items": food_items
    }

@router.get("/daily_nutrition", response_model=DailyNutritionResponse, summary='Получить информацию о питании за день')
async def get_daily_nutrition(
    target_date: date,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await MealDAO(session).get_daily_nutrition(user.id, target_date)


@router.get("/daily_meals", response_model=DailyMealsResponse, summary="Получить все приемы пищи за день с продуктами")
async def get_daily_meals(
    target_date: date,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await MealDAO(session).get_daily_meals(user.id, target_date)


@router.get("/search_item", response_model=List[FoodItemResponse], summary="Поиск схожих продуктов")
async def search_foods(
    query: str = Query(..., min_length=2, max_length=50),
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_async_session)
):
    '''Поиск продуктов питания'''
    return await FoodItemDAO(session).search_foods(query=query, limit=limit)


@router.delete("/delete_meal", summary="Удалить прием пищи по типу и дате")
async def delete_meal(
    mealtime: str,
    meal_date: date,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    await MealDAO(session).delete_meal_by_type_and_date(
        mealtime=mealtime,
        meal_date=meal_date,
        user_id=user.id
    )
    return {"message": "Прием пищи успешно удален!"}


@router.post("/food_items",summary="Добавить новый продукт(is_superuser)")
async def create_food_item(
    food_data: FoodItemCreate,
    admin: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Добавление нового продукта (только для администраторов)"""
    food_item = await FoodItemDAO(session).create_food_item(food_data)
    return {"message": "Продукт успешно добавлен"}

