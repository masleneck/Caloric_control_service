from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class TestResultCreate(BaseModel):
    '''Схема для сохранения результатов теста'''
    user_id: int  # ID пользователя
    answers: dict  # JSON с ответами пользователя

    model_config = ConfigDict(from_attributes=True) 

class TestResultResponse(TestResultCreate):
    '''Схема ответа API с результатами теста'''
    id: int  # ID записи теста
    date_taken: date  # Дата прохождения теста
    fitness_level: Optional[str] = None  # Уровень физической подготовки
    recommended_calories: Optional[float] = None  # Рассчитанная норма калорий

    model_config = ConfigDict(from_attributes=True) 
