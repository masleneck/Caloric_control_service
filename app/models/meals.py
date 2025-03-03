from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='meals')
    food_items = relationship('MealFoodItem', back_populates='meal', cascade='all, delete-orphan')
class MealFoodItem(Base):
    """Связь приемов пищи и продуктов"""
    __tablename__ = 'meal_food_items'

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey('meals.id', ondelete='CASCADE'))
    food_item_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'))
    quantity = Column(Float, nullable=False)  

    meal = relationship('Meal', back_populates='food_items')
    food_item = relationship('FoodItem', back_populates='meal_associations')
