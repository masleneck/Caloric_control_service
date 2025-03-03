from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.db import Base


class UserGoal(enum.Enum):
    '''Цели пользователя'''
    LOSE_WEIGHT = 'lose weight' # похудение
    KEEPING_FIT = 'keeping fit' # поддержание формы
    GAIN_MUSCLE_MASS = 'gain muscle mass' # набрать мышечную массу


class UserGoalHistory(Base):
    """История целей пользователя"""
    __tablename__ = 'user_goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    goal = Column(Enum(UserGoal), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)  

    user = relationship('User', back_populates='goals')
