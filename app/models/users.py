'''
Column - используется для описания полей таблицы
Integer, String - типы данных столбцов (числовые и строковые значения)
declarative_base - создает базовый класс для моделей
'''
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Float
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
    '''Храним информацию о пользователях'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey('goals.id'), nullable=True)  # Связь с целями
    name = Column(String, nullable=False) # Имя
    email = Column(String, unique=True, index=True, nullable=False) # Почта
    username = Column(String, unique=True, index=True, nullable=False) # Никнейм
    hashed_password = Column(String, nullable=False)  # Храним только хеш пароля
    birthday_date = Column(Date, nullable=True) # Дата рождения
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False) # Роль(admin)

    weight = Column(Float, nullable=True)  # Вес в кг
    height = Column(Integer, nullable=True)  # Рост в см
    gender = Column(Enum(Gender), nullable=True)  # Пол
    activity_level = Column(Enum(ActivityLevel), nullable=True)  # Уровень активности

    goal = relationship('Goal', back_populates='users', uselist=False) 
    test_results = relationship('TestResult', back_populates='user', cascade='all, delete-orphan')
    workouts = relationship('Workout', back_populates='user', cascade='all, delete-orphan')
    meals = relationship('Meal', back_populates='user', cascade='all, delete-orphan')


