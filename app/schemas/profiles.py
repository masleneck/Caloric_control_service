from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.models import Gender
class ProfileInfoResponse(BaseModel):
    name: str 
    last_name: str 
    gender: Gender 
    weight: float 
    height: int 
    birthday_date: Optional[date] 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'name': 'Амаль',
            'last_name': 'Габидов',
            'gender': Gender.MALE,
            'weight': 59,
            'height': 178,
            'birthday_date': '2002-08-01'
        }
    })
class UpdateProfileRequest(BaseModel):
    name: str 
    last_name: str 
    gender: Gender 
    weight: float 
    height: int 
    birthday_date: Optional[date] 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'name': 'Амаль',
            'last_name': 'Габидов',
            'gender': Gender.MALE,
            'weight': 59,
            'height': 178,
            'birthday_date': '2002-08-01'
        }
    })

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
    full_name: str 
    model_config = ConfigDict(from_attributes=True)