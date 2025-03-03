from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Workout(Base):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories_burned = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    user_workouts = relationship('UserWorkout', back_populates='workout', cascade='all, delete-orphan')

class UserWorkout(Base):
    """Связь пользователей и тренировок"""
    __tablename__ = 'user_workouts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    workout_id = Column(Integer, ForeignKey('workouts.id', ondelete='CASCADE'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='workouts')
    workout = relationship('Workout', back_populates='user_workouts')
