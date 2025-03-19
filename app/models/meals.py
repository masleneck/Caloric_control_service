from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.data.db import Base

class Mealtime(enum.Enum):
    '''Тип приема пищи'''
    BREAKFAST = 'BREAKFAST'
    LUNCH = 'LUNCH'
    DINNER = 'DINNER'
    NOT_STATED = 'NOT_STATED'

class Meal(Base):
    '''Хранит приемы пищи'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    mealtime: Mapped[Mealtime] = mapped_column(default = Mealtime.NOT_STATED, server_default = text('"NOT_STATED"'))
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
        back_populates='meals',
        overlaps='meal_food_links'
    )

    # Связь один-ко-многим с MealFoodItem 
    meal_food_links: Mapped[list['MealFoodItem']] = relationship(
        'MealFoodItem',
        back_populates='meal',
        cascade='all, delete-orphan',
        overlaps='food_items'
    )