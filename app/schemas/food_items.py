from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class FoodCreate(BaseModel):
    '''Схема для добавления нового продукта (параметры на 100 г)'''
    name: str = Field(..., max_length=50, title='Название продукта')
    calories: float = Field(..., ge=0, title='Калорийность (г)')
    proteins: float = Field(..., ge=0, title='Белки (г)')
    fats: float = Field(..., ge=0, title='Жиры (г)')
    carbs: float = Field(..., ge=0, title='Углеводы (г)')

    model_config = ConfigDict(from_attributes=True)


class FoodUpdate(BaseModel):
    '''Схема для обновления нового продукта (параметры на 100 г)'''
    name: Optional[str] = Field(max_length=50, title='Название продукта')
    calories: Optional[float] = Field(ge=0, title='Калорийность (г)')
    proteins: Optional[float] = Field(None, ge=0, title='Белки (г)')
    fats: Optional[float] = Field(None, ge=0, title='Жиры (г)')
    carbs: Optional[float] = Field(None, ge=0, title='Углеводы (г)')

    model_config = ConfigDict(from_attributes=True)

class FoodResponse(FoodCreate):
    '''Схема ответа API с продуктами питания'''
    id: int
    name: str
    calories: float
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


'''
Как будем считать калорийность и БЖУ?
При выдаче данных в API мы будем автоматически рассчитывать калорийность и БЖУ на основе food_items.

Формула расчёта:

Если в food_items хранится БЖУ на 100 грамм, то:
калории = (калории на 100г / 100) * quantity
белки = (белки на 100г / 100) * quantity
жиры = (жиры на 100г / 100) * quantity
углеводы = (углеводы на 100г / 100) * quantity
'''