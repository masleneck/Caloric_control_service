from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models import Mealtime


class BaseFoodItem(BaseModel):
    id: int
    name: str

# Упрощенное представление связи продукта с приемом пищи
class MealFoodItem(BaseModel):
    food_item: BaseFoodItem
    quantity: float

# Упрощенное представление приема пищи
class BaseMeal(BaseModel):
    id: int
    user_id: int
    mealtime: Mealtime
    meal_date: date
    food_items: List[MealFoodItem]


# Схема для информации о питании
class NutritionalInfo(BaseModel):
    calories: float
    proteins: float
    fats: float
    carbs: float

class MealProductsResponse(BaseModel):
    '''Схема для возврата mealtime и списка имен продуктов.'''
    mealtime: Mealtime
    products: List[str]  

class MealUpdateRequest(BaseModel):
    '''Схема для обновления/создания приема пищи.'''
    mealtime: Mealtime
    meal_date: date
    names: List[str] = Field(..., description='Список названий продуктов')
    quantities: List[float] = Field(..., description='Список количеств продуктов')