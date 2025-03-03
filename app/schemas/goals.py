from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

from app.models.goals import UserGoal

class GoalBase(BaseModel):
    '''Базовая схема для целей (общие поля)'''
    name: UserGoal
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) 


class GoalUpdate(GoalBase):
    '''Схема для обновления цели'''
    name: UserGoal = Field(example='keepeing fit')
    description: Optional[str] = Field(None, max_length=300, title='Описание',example='Хочу поддерживать свою форму в норме!')

    model_config = ConfigDict(from_attributes=True) 


class GoalResponse(GoalBase):
    '''Схема для ответа (с id)'''
    id: int
    name: UserGoal 
    description: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True) 

