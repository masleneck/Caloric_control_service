from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.data.db import Base

class Mealtime(enum.Enum):
    '''Тип приема пищи'''
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'
    NOT_STATED = 'not stated'

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
        back_populates='meals'
    )

    # Связь один-ко-многим с MealFoodItem 
    meal_food_links: Mapped[list['MealFoodItem']] = relationship(
        'MealFoodItem',
        back_populates='meal',
        cascade='all, delete-orphan'
    )


    def to_pydantic(self):
        '''Преобразует объект SQLAlchemy в словарь, совместимый с MealSimple'''
        return {
            'id': self.id,
            'user_id': self.user_id,
            'mealtime': self.mealtime.value,  # Преобразуем Enum в строку
            'meal_date': self.meal_date.date(), # <-- Преобразуем datetime в date
            'food_items': [
                {
                    'food_item': {
                        'id': link.food_item.id,
                        'name': link.food_item.name,  # Только id и name
                    },
                    'quantity': link.quantity,
                }
                for link in self.meal_food_links
            ],
        }