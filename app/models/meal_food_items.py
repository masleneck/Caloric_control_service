from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db import Base

class MealFoodItem(Base):
    '''Связь приемов пищи и продуктов'''
    __tablename__ = 'meal_food_items'

    meal_id: Mapped[int] = mapped_column(ForeignKey('meals.id'))
    food_item_id: Mapped[int] = mapped_column(ForeignKey('food_items.id'))
    quantity: Mapped[float]


