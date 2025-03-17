from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.data.db import Base

class Gender(enum.Enum):
    '''Пол пользователя'''
    MALE = 'male'
    FEMALE = 'female'
    NOT_STATED = 'not stated'

class CurrentGoal(enum.Enum):
    '''Цели пользователя'''
    LOSE_WEIGHT = 'lose weight' # похудение
    KEEPING_FIT = 'keeping fit' # поддержание формы
    GAIN_MUSCLE_MASS = 'gain muscle mass' # набрать мышечную массу
    NOT_STATED = 'not stated'

class ActivityLevel(enum.Enum):
    '''Уровень активности пользователя'''
    SEDENTARY = 'sedentary'  # Малоподвижный образ жизни
    LIGHT = 'light'  # Легкая активность (1-3 тренировки в неделю)
    MODERATE = 'moderate'  # Средняя активность (3-5 тренировок в неделю)
    ACTIVE = 'active'  # Высокая активность (6-7 тренировок в неделю)
    ATHLETE = 'athlete'  # Спортсмен
    NOT_STATED= 'not stated'

class Profile(Base):
    '''Хранит информацию пользователя'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    last_name: Mapped[str | None]
    gender: Mapped[Gender] = mapped_column(default = Gender.NOT_STATED, server_default = text("'NOT_STATED'"))
    weight: Mapped[float]
    height: Mapped[int]
    goal: Mapped[CurrentGoal] = mapped_column(default = CurrentGoal.NOT_STATED, server_default = text("'NOT_STATED'"))
    birthday_date: Mapped[datetime | None] = mapped_column(DateTime)
    activity_level: Mapped[ActivityLevel] = mapped_column(default = ActivityLevel.NOT_STATED, server_default = text("'NOT_STATED'"))

    
    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
    'User',
    back_populates='profile',
    uselist=False
    )