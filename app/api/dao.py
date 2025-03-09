from typing import Optional
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.schemas.users import UserBase
from app.dao.base import BaseDAO
from app.models import User, Profile, Workout, WorkoutInfo, Meal, MealFoodItem, FoodItem, TestQuestion, TestResult


class UserDAO(BaseDAO):
    model = User

class ProfileDAO(BaseDAO):
    model = Profile

class WorkoutDAO(BaseDAO):
    model = Workout

class WorkoutInfoDAO(BaseDAO):
    model = WorkoutInfo

class MealDAO(BaseDAO):
    model = Meal

class MealFoodItemDAO(BaseDAO):
    model = MealFoodItem

class FoodItemDAO(BaseDAO):
    model = FoodItem

class TestQuestionDAO(BaseDAO):
    model = TestQuestion

class TestResultDAO(BaseDAO):
    model = TestResult