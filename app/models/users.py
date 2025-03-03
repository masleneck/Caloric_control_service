'''
Column - используется для описания полей таблицы
Integer, String - типы данных столбцов (числовые и строковые значения)
declarative_base - создает базовый класс для моделей
'''
from sqlalchemy import Column, Integer, String, Date, Enum, Float
from sqlalchemy.orm import relationship
import enum

from app.core.db import Base

class UserRole(enum.Enum):
    '''Роли'''
    USER = 'user'
    ADMIN = 'admin'

class ActivityLevel(enum.Enum):
    '''Уровень активности пользователя'''
    SEDENTARY = 'sedentary'  # Малоподвижный образ жизни
    LIGHT = 'light'  # Легкая активность (1-3 тренировки в неделю)
    MODERATE = 'moderate'  # Средняя активность (3-5 тренировок в неделю)
    ACTIVE = 'active'  # Высокая активность (6-7 тренировок в неделю)
    ATHLETE = 'athlete'  # Спортсмен

class Gender(enum.Enum):
    '''Пол пользователя'''
    MALE = 'male'
    FEMALE = 'female'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    birthday_date = Column(Date, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    weight = Column(Float, nullable=True)
    height = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    activity_level = Column(Enum(ActivityLevel), nullable=True)

    test_results = relationship('TestResult', back_populates='user', cascade='all, delete-orphan')
    workouts = relationship('UserWorkout', back_populates='user', cascade='all, delete-orphan')
    meals = relationship('Meal', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('UserGoalHistory', back_populates='user', cascade='all, delete-orphan')



