from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Literal
from datetime import date
from app.models import Gender, CurrentGoal

class TestQuestionResponse(BaseModel):
    id: int
    name: str
    text: str
    type: str
    options: Optional[List[str]]
    model_config = ConfigDict(from_attributes=True)


class MetricsRequest(BaseModel):
    gender: Gender
    birthday_date: date
    height: int 
    weight: int 
    goal: CurrentGoal
    bad_habits: Literal['Да', 'Нет']
    steps_per_day: int 
    sleep_hours: int 
    water_intake: Literal['Менее 0,5л', '0,5-1,5л', '1.5-3л', 'Более 3л']
    hormone_issues: Literal['Нет / Никогда не сдавал анализы',
                            'Гипотиреоз',
                            'Лептинорезистентность/Инсулинорезистентность',
                            'Дефициты половых гормонов и различные активные компенсаторные механизмы',
                            'Различные эндокринные нарушения'
                            ]
    model_config = ConfigDict(from_attributes=True, use_enum_values=True, json_schema_extra={
        'example': {
            'goal': CurrentGoal.GAIN_MUSCLE_MASS,
            'gender': Gender.MALE,
            'weight': 59,
            'height': 178,
            'birthday_date': '2002-08-01',
            'bad_habits': 'Да',
            'steps_per_day': 5000,
            'sleep_hours': 8,
            'water_intake': '1.5-3л',
            'hormone_issues': 'Нет / Никогда не сдавал анализы'
        }
    })