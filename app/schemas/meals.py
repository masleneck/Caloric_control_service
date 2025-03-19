from datetime import date
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Annotated
from app.models import Mealtime


class BaseFoodItem(BaseModel):
    '''Базовая схема для продукта.'''
    id: int 
    name: str 
    model_config = ConfigDict(from_attributes=True) 


class MealFoodItem(BaseModel):
    '''Схема для связи продукта с приемом пищи.'''
    food_item: BaseFoodItem 
    quantity: Annotated[float, Field(ge=0)]
    model_config = ConfigDict(from_attributes=True)
    
class BaseMeal(BaseModel):
    '''Базовая схема для приема пищи.'''
    id: int 
    user_id: int
    mealtime: Mealtime 
    meal_date: date 
    food_items: List[MealFoodItem]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True) 

class NutritionalInfo(BaseModel):
    '''Схема для информации о питательной ценности.'''
    calories: Annotated[float, Field(ge=0)] 
    proteins: Annotated[float, Field(ge=0)] 
    fats: Annotated[float, Field(ge=0)] 
    carbs: Annotated[float, Field(ge=0)] 
    model_config = ConfigDict(from_attributes=True)

class MealProductsResponse(BaseModel):
    '''Схема для возврата информации о приеме пищи.'''
    meal_id: int 
    mealtime: Mealtime
    products: List[str]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'meal_id': 1,
            'mealtime': Mealtime.BREAKFAST,
            'products': ['Банан','Творог 5%'],
        }
    })

class MealUpdateRequest(BaseModel):
    '''Схема для обновления или создания приема пищи.'''
    mealtime: Mealtime 
    meal_date: date 
    names: List[str] = Field(min_length=1)
    quantities: List[Annotated[float, Field(ge=0)]] = Field(min_length=1)
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'mealtime': Mealtime.BREAKFAST,
            'meal_date': date.today().isoformat(),
            'names': ['Банан','Творог 5%'],
            'quantities': [100.0, 50.0],
        }
    })

    @field_validator('meal_date')
    def validate_meal_date(cls, value: date) -> date:
        '''Проверка, что дата не позже текущей.'''
        if value > date.today():
            raise ValueError('Дата приема пищи не может быть позже текущей даты')
        return value

