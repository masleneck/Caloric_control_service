'''
Pydantic модель нужна для того, чтобы валидировать и структурировать входящие данные в соответствии с заданными типами.
Pydantic позволяет легко описывать схему данных и выполнять автоматическую проверку типов,
а также трансформировать значения в нужный формат при необходимости.
'''

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.profiles import Gender, СurrentGoal, ActivityLevel


class ProfilePydantic(BaseModel):
    name: str
    gender: Gender
    weight: float
    height: int
    goal: СurrentGoal
    birthday_date: datetime | None
    activity_level: ActivityLevel

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    # from_attributes = True: это позволяет модели автоматически маппить атрибуты Python объектов на поля модели. 
    # Примерно то что мы делали в методе to_dict, но более расширенно.

    # use_enum_values = True: это указание преобразовывать значения перечислений в их фактические значения, 
    # а не в объекты перечислений. Просто для удобства восприятия человеком.

class UserPydantic(BaseModel):
    email: str
    username: str
    profile: ProfilePydantic | None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class UsernameIdPydantic(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)