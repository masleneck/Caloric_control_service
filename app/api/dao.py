from typing import Optional
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.schemas.users import UserBase
from app.dao.base import BaseDAO
from app.models import Meal, MealFoodItem, FoodItem

class MealDAO(BaseDAO):
    model = Meal

class MealFoodItemDAO(BaseDAO):
    model = MealFoodItem

class FoodItemDAO(BaseDAO):
    model = FoodItem
