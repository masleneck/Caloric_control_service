from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from app.models.meals import Mealtime

class FoodItemShortResponse(BaseModel):
    id: int
    name: str
    calories: float
    proteins: float
    fats: float
    carbs: float

class MealFoodItemResponse(BaseModel):
    id: int
    meal_id: int
    food_item: FoodItemShortResponse
    quantity: float

    model_config = ConfigDict(from_attributes=True)

class MealDetailResponse(BaseModel):
    id: int
    mealtime: Mealtime
    meal_date: datetime
    total_calories: float = Field(..., description='Суммарная калорийность')
    food_items: List[MealFoodItemResponse]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_encoders = {datetime: lambda v: v.isoformat()})


class MealCreate(BaseModel):
    food_item_id: int = Field(..., gt=0)
    mealtime: Mealtime
    meal_date: datetime
    quantity: float = Field(..., gt=0)

    @field_validator('meal_date')
    def validate_date(cls, v):
        if v > datetime.now():
            raise ValueError('Дата не может быть в будущем')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'food_item_id': 1,
                'mealtime': 'breakfast',
                'meal_date': '2024-04-20 06:59:59',
                'quantity': 150.5
            }
        }
    )

class MealCreateResponse(BaseModel):
    message: str
    meal_id: int
    model_config = ConfigDict(from_attributes=True,json_schema_extra={
            'example': {
                'message': 'Прием пищи под ID 5 добавлен успешно!',
                'meal_id': 5
            }
        }
    )
