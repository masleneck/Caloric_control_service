from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.core.db import Base

class Workout(Base):
    '''Храним информацию о тренировках'''
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String, nullable=False) # Название тренировки
    duration_minutes = Column(Integer, nullable=False) # Длительность тренировки
    calories_burned = Column(Float, nullable=False) # Калории
    date = Column(Date, nullable=True) # Дата
    description = Column(String, nullable=True) # Описание



    user = relationship('User', back_populates='workouts')
