from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models import Gender
class ProfileInfoResponse(BaseModel):
    name: str = Field(..., description='Имя пользователя', example='Амаль')
    last_name: str = Field(..., description='Фамилия пользователя', example='Габидов')
    gender: Gender = Field(..., description='Пол пользователя', example=Gender.MALE)
    weight: float = Field(..., description='Вес пользователя в кг', example=59)
    height: int = Field(..., description='Рост пользователя в см', example=178)
    birthday_date: Optional[date] = Field(None, description='Дата рождения пользователя', example='2002-08-01')

class UpdateProfileRequest(BaseModel):
    name: str = Field(..., description='Имя пользователя', example='Амаль')
    last_name: str = Field(..., description='Фамилия пользователя', example='Габидов')
    gender: Gender = Field(..., description='Пол пользователя', example=Gender.MALE)
    weight: float = Field(..., description='Вес пользователя в кг', example=59)
    height: int = Field(..., description='Рост пользователя в см', example=178)
    birthday_date: Optional[date] = Field(None, description='Дата рождения пользователя', example='2002-08-01')

    @field_validator('weight')
    def validate_weight(cls, value):
        '''Проверяет, что вес положительный.'''
        if value <= 0:
            raise ValueError('Вес должен быть положительным числом')
        return value

    @field_validator('height')
    def validate_height(cls, value):
        '''Проверяет, что рост положительный.'''
        if value <= 0:
            raise ValueError('Рост должен быть положительным числом')
        return value

class FullNameResponse(BaseModel):
    '''Схема для ответа с полным именем пользователя.'''
    full_name: str = Field(..., description='Полное имя пользователя (имя + фамилия)', example='Амаль Габидов') 