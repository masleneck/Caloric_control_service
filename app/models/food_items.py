from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.db import Base

class FoodItem(Base):
    '''Храним информацию о продуктах'''
    __tablename__ = 'food_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Название продукта
    calories = Column(Float, nullable=False)  # Калории на 100 г
    proteins = Column(Float, nullable=True)  # Белки
    fats = Column(Float, nullable=True)  # Жиры
    carbs = Column(Float, nullable=True)  # Углеводы

    meals = relationship('Meal', back_populates='food')
