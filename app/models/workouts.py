from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base


class Workout(Base):
    '''Связь пользователей и их тренировок'''
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    workout_info_id = Column(Integer, ForeignKey('workouts_info.id', ondelete='CASCADE'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='workouts')
    workout_info = relationship('WorkoutInfo', back_populates='workouts')


class WorkoutInfo(Base):
    '''Хранит информацию о тренировках'''
    __tablename__ = 'workouts_info'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    workouts = relationship('Workout', back_populates='workout_info', cascade='all, delete-orphan')
