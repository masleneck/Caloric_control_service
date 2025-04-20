from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import date
from typing import Dict, List
from app.models import Mealtime

class MealUpsertRequest(BaseModel):
    mealtime: Mealtime
    meal_date: date
    food_names: List[str] = Field(..., min_items=1)
    food_quantities: List[float] = Field(..., min_items=1)
    
    @field_validator('food_quantities')
    def validate_quantities(cls, v):
        if any(q <= 0 for q in v):
            raise ValueError("Все количества должны быть положительными")
        return v
    
    @field_validator('food_names', 'food_quantities')
    def validate_length_match(cls, v, info):
        if info.field_name == 'food_names':
            if 'food_quantities' in info.data and len(v) != len(info.data['food_quantities']):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Количество продуктов и граммовок должно совпадать"
                )
        return v

    model_config = ConfigDict(from_attributes=True)


class MealResponse(BaseModel):
    id: int
    mealtime: Mealtime
    meal_date: date
    food_items: List[dict]  # {name: str, quantity: float}
    
    model_config = ConfigDict(from_attributes=True)


class DailyNutritionResponse(BaseModel):
    total_calories: float = 0.0
    total_proteins: float = 0.0
    total_fats: float = 0.0
    total_carbs: float = 0.0
    
    @field_validator('total_calories', 'total_proteins', 'total_fats', 'total_carbs', mode='after')
    def round_values(cls, v: float) -> float:
        return round(v, 2)
    
    model_config = ConfigDict(from_attributes=True)


class MealProductsResponse(BaseModel):
    mealtime: Mealtime 
    products: List[str]


class DailyMealsResponse(BaseModel):
    date: date
    meals: Dict[Mealtime, MealProductsResponse]  
    
    model_config = ConfigDict(from_attributes=True)


class FoodItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    calories: float = Field(..., gt=0)
    proteins: float = Field(..., gt=0)
    fats: float = Field(..., gt=0)
    carbs: float = Field(..., gt=0)
    
    model_config = ConfigDict(from_attributes=True)

class FoodItemResponse(BaseModel):
    id: int
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)