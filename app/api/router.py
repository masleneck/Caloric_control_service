from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from loguru import logger

from app.api.dao.food_item import FoodItemDAO
from app.api.dao.meal import MealDAO
from app.api.dao.meal_food_item import MealFoodItemDAO
from app.schemas.meals import FoodItemCreate, MealCreate, MealFoodItemCreate
from app.dao.session_maker import SessionDep

router = APIRouter(prefix='/api', tags=['Nutrition'])


@router.post("/food/", summary="Добавление нового продукта")
async def add_food_item(food_data: FoodItemCreate, session: AsyncSession = SessionDep):
    try:
        food_id = await FoodItemDAO.add_food_item(session, food_data.model_dump())
        return {"status": "success", "food_id": food_id}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Продукт с таким именем уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении продукта: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при добавлении продукта.")


@router.post("/meals/", summary="Добавление приема пищи")
async def add_meal(meal_data: MealCreate, session: AsyncSession = SessionDep):
    try:
        meal_id = await MealDAO.add_meal(session, meal_data.user_id, meal_data.mealtime, meal_data.meal_date)
        return {"status": "success", "meal_id": meal_id}
    except Exception as e:
        logger.error(f"Ошибка при добавлении приема пищи: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при добавлении приема пищи.")


@router.post("/meals/{meal_id}/food/", summary="Добавление продукта в прием пищи")
async def add_food_to_meal(meal_id: int, food_data: MealFoodItemCreate, session: AsyncSession = SessionDep):
    try:
        await MealFoodItemDAO.add_food_to_meal(session, meal_id, food_data.food_item_id, food_data.quantity)
        return {"status": "success", "message": "Продукт успешно добавлен в прием пищи"}
    except Exception as e:
        logger.error(f"Ошибка при добавлении продукта в прием пищи: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при добавлении продукта в прием пищи.")
