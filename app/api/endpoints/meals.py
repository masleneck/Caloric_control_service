from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.food_items import FoodItems
from app.models.users import User
from app.repositories.food_item import FoodItemDAO
from app.repositories.meal import MealDAO
from app.dependencies.database_dep import get_async_session
from app.dependencies.auth_dep import get_current_admin_user, get_current_user
from app.schemas.meals import DailyMealsResponse, DailyNutritionResponse, FoodItemCreate, MealResponse, MealUpsertRequest

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


@router.post("/food-items",summary="Добавить новый продукт(is_superuser)")
async def create_food_item(
    food_data: FoodItemCreate,
    admin: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Добавление нового продукта (только для администраторов)"""
    food_item = await FoodItemDAO(session).create_food_item(food_data)
    return {"message": "Продукт успешно добавлен"}
