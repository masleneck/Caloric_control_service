from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.db import Base

class Mealtime(enum.Enum):
    '''Тип приема пищи'''
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    NOT_STATED = 'not stated'

class Meal(Base):
    '''Хранит приемы пищи'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    mealtime: Mapped[Mealtime] = mapped_column(default = Mealtime.NOT_STATED, server_default = text("'NOT_STATED'"))
    meal_date: Mapped[datetime] = mapped_column(DateTime)

    
    # Связь многие-к-одному с User
    user: Mapped['User'] = relationship(
        'User',
        back_populates='meals'
    )

    # Связь многие-ко-многим с FoodItem через MealFoodItem
    food_items: Mapped[list['FoodItem']] = relationship(
        'FoodItem',
        secondary='meal_food_items',  # имя промежуточной таблицы
        back_populates='meals'
    )

