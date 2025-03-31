from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict
from app.models import Gender, CurrentGoal
class ProfileInfoResponse(BaseModel):
    name: str 
    last_name: str 
    gender: Gender 
    weight: float 
    height: int 
    goal: CurrentGoal 
    birthday_date: Optional[date]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'name': 'Амаль',
            'last_name': 'Габидов',
            'gender': Gender.MALE,
            'weight': 59,
            'height': 178,
            'goal': CurrentGoal.GAIN_MUSCLE_MASS,
            'birthday_date': '2002-08-01'
        }
    })
class UpdateProfileRequest(BaseModel):
    name: str | None = None
    last_name: str | None = None
    gender: Gender 
    weight: float | None = None
    height: int | None = None
    goal: CurrentGoal 
    birthday_date: Optional[date] 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'name': 'Амаль',
            'last_name': 'Габидов',
            'gender': Gender.MALE,
            'weight': 59,
            'height': 178,
            'goal': CurrentGoal.GAIN_MUSCLE_MASS,
            'birthday_date': '2002-08-01'
        }
    })


class FullNameResponse(BaseModel):
    '''Схема для ответа с полным именем пользователя.'''
    full_name: str 
    model_config = ConfigDict(from_attributes=True)