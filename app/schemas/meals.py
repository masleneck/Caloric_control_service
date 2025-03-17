from datetime import date
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Annotated
from app.models import Mealtime


class BaseFoodItem(BaseModel):
    '''Базовая схема для продукта.'''
    id: int = Field(..., description='Уникальный идентификатор продукта', example=1)
    name: str = Field(..., description='Название продукта', example='Банан')

class MealFoodItem(BaseModel):
    '''Схема для связи продукта с приемом пищи.'''
    food_item: BaseFoodItem = Field(..., description='Продукт')
    quantity: Annotated[float, Field(gt=0)] = Field(..., description='Количество продукта в граммах', example=100.0)
    
class BaseMeal(BaseModel):
    '''Базовая схема для приема пищи.'''
    id: int = Field(..., description='Уникальный идентификатор приема пищи', example=1)
    user_id: int = Field(..., description='Идентификатор пользователя', example=1)
    mealtime: Mealtime = Field(..., description='Тип приема пищи', example=Mealtime.BREAKFAST)
    meal_date: date = Field(..., description='Дата приема пищи', example='2023-10-01')
    food_items: List[MealFoodItem] = Field(..., description='Список продуктов в приеме пищи')

class NutritionalInfo(BaseModel):
    '''Схема для информации о питательной ценности.'''
    calories: Annotated[float, Field(gt=0)] = Field(..., description='Калории (ккал)', example=250.0)
    proteins: Annotated[float, Field(gt=0)] = Field(..., description='Белки (г)', example=10.0)
    fats: Annotated[float, Field(gt=0)] = Field(..., description='Жиры (г)', example=5.0)
    carbs: Annotated[float, Field(gt=0)] = Field(..., description='Углеводы (г)', example=30.0)

class MealProductsResponse(BaseModel):
    '''Схема для возврата информации о приеме пищи.'''
    meal_id: int = Field(..., description='Уникальный идентификатор приема пищи', example=1)
    mealtime: Mealtime = Field(..., description='Тип приема пищи', example=Mealtime.BREAKFAST)
    products: List[str] = Field(..., description='Список названий продуктов', example=['Банан', 'Творог 5%'])

class MealUpdateRequest(BaseModel):
    '''Схема для обновления или создания приема пищи.'''
    mealtime: Mealtime = Field(..., description='Тип приема пищи', example=Mealtime.BREAKFAST)
    meal_date: date = Field(..., description='Дата приема пищи')
    names: List[str] = Field(..., description='Список названий продуктов', example=['Банан', 'Творог 5%'], min_length=1)
    quantities: List[Annotated[float, Field(ge=0)]] = Field(..., description='Список количеств продуктов в граммах', example=[100.0, 50.0], min_length=1)

    @field_validator('meal_date')
    def validate_meal_date(cls, value: date) -> date:
        '''Проверка, что дата не позже текущей.'''
        if value > date.today():
            raise ValueError('Дата приема пищи не может быть позже текущей даты')
        return value

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'mealtime': Mealtime.BREAKFAST,
                'meal_date': date.today().isoformat(),
                'names': ['Банан', 'Творог 5%'],
                'quantities': [100.0, 50.0],
            }
        }
    )