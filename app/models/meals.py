from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base

class Meal(Base):
    '''Храним информацию о приемах пищи'''
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    food_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'))
    quantity = Column(Float, nullable=False)  # Количество в граммах
    datetime = Column(DateTime, default=datetime.utcnow)  # Время приёма пищи

    user = relationship('User', back_populates='meals')
    food = relationship('FoodItem', back_populates='meals')
