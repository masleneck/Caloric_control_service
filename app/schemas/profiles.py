from datetime import date
from pydantic import BaseModel


class ProfileInfoResponse(BaseModel):
    name: str
    last_name: str
    gender: str
    weight: float
    height: int
    birthday_date: date


class UpdateProfileRequest(BaseModel):
    name: str
    last_name: str
    gender: str
    weight: float
    height: int
    birthday_date: date

class FullNameResponse(BaseModel):
    '''Схема для ответа с полным именем пользователя.'''
    full_name: str  