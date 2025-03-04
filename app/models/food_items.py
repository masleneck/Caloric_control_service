from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.db import Base

class FoodItem(Base):
    '''Хранит продукты'''
    __tablename__ = 'food_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    calories = Column(Float, nullable=False)
    proteins = Column(Float, nullable=False, default=0.0)
    fats = Column(Float, nullable=False, default=0.0)
    carbs = Column(Float, nullable=False, default=0.0)

    meals = relationship('MealFoodItem', back_populates='food_item', cascade='all, delete-orphan')
