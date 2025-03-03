from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date as d
from typing import Optional

class WorkoutCreate(BaseModel):
    '''Схема для создания тренировки'''
    name: str = Field(..., max_length=50)  # Ограничиваем длину 50
    duration_minutes: int = Field(..., ge=1, le=300)  # От 1 до 300 минут
    calories_burned: float = Field(..., ge=0)  # Не может быть меньше 0
    date: Optional[d] = None  # Дата тренировки (по умолчанию None)
    description: str = Field(..., max_length=300) # Ограничиваем длину 300

    model_config = ConfigDict(from_attributes=True)

class WorkoutUpdate(BaseModel):
    '''Схема для обновления тренировки'''
    name: Optional[str] = Field(max_length=50)  # Ограничиваем длину 50
    duration_minutes: Optional[int] = Field(ge=1, le=300)  # От 1 до 300 минут
    calories_burned: Optional[float] = Field(ge=0)  # Не может быть меньше 0
    date: Optional[d] = None  # Дата тренировки (по умолчанию None)
    description: Optional[str] = Field(None, max_length=300) # Ограничиваем длину 300

    model_config = ConfigDict(from_attributes=True)    

 
class WorkoutResponse(WorkoutCreate):
    '''Схема ответа API с тренировками'''
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
