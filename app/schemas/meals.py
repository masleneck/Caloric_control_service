from pydantic import BaseModel, ConfigDict, Field, field_serializer
from datetime import datetime as dt
from typing import Optional


class MealCreate(BaseModel):
    '''Схема для создания приема пищи'''
    food_id: int  # ID продукта из food_items
    quantity: float = Field(gt=0, description='Количество в граммах')  # Количество продукта

    model_config = ConfigDict(from_attributes=True) 


class MealUpdate(BaseModel):
    '''Схема для обновления информации о приеме пищи'''
    food_id: int  # ID продукта из food_items
    quantity: float = Field(gt=0, description='Количество в граммах')  # Количество продукта
    datetime: Optional[dt] = None

    model_config = ConfigDict(from_attributes=True)


class MealResponse(BaseModel):
    '''Схема ответа API с расчетом калорий, белков, жиров и углеводов'''
    id: int
    food_id: int
    quantity: float
    datetime: dt
    food_name: str  # Название продукта
    calories: float
    proteins: float
    fats: float
    carbs: float

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('datetime')
    def serialize_datetime(self, dt: dt, _info) -> str:
        '''Автоматически форматирует дату при возврате в API'''
        return dt.strftime('%d-%m-%Y %H:%M')
