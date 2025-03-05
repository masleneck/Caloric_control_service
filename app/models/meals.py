from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

class Meal(Base):
    '''Хранит приемы пищи'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(server_default = func.now()) 
    
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

