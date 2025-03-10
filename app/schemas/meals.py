from pydantic import BaseModel
from datetime import datetime

class FoodItemCreate(BaseModel):
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float

class MealCreate(BaseModel):
    user_id: int
    mealtime: str
    meal_date: datetime

class MealFoodItemCreate(BaseModel):
    meal_id: int
    food_item_id: int
    quantity: float