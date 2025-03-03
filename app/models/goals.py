from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import enum

from app.core.db import Base


class UserGoal(enum.Enum):
    '''Цели пользователя'''
    LOSE_WEIGHT = 'lose weight' # похудение
    KEEPEING_FIT = 'keepeing fit' # поддержание формы
    GAIN_MUSCLE_MASS = 'gain muscle mass' # набрать мышечную массу

class Goal(Base):
    '''Храним возможные цели'''
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) # Цели
    description = Column(String, nullable=True) # Описание

    users = relationship('User', back_populates='goal')
