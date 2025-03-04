from sqlalchemy import Column, Integer, String, Date, Enum, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.core.db import Base


class User(Base):
    '''Хранит информацию для авторизации'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Связь с профилем, активностью и целью;  uselist=False один к одному
    profile = relationship('UserProfile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    activity = relationship('UserActivity', uselist=False, back_populates='user', cascade='all, delete-orphan')
    goal = relationship('UserGoal', uselist=False, back_populates='user', cascade='all, delete-orphan')
    # Связь с другими таблицами
    test_results = relationship('TestResult', back_populates='user', cascade='all, delete-orphan')
    workouts = relationship('UserWorkout', back_populates='user', cascade='all, delete-orphan')
    meals = relationship('Meal', back_populates='user', cascade='all, delete-orphan')


class UserRole(enum.Enum):
    '''Роли'''
    USER = 'user'
    ADMIN = 'admin'


class Gender(enum.Enum):
    '''Пол пользователя'''
    MALE = 'male'
    FEMALE = 'female'


class UserProfile(Base):
    '''Хранит информацию пользователя'''
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)
    birthday_date = Column(Date, nullable=True)

    user = relationship('User', back_populates='profile')


class ActivityLevel(enum.Enum):
    '''Уровень активности пользователя'''
    SEDENTARY = 'sedentary'  # Малоподвижный образ жизни
    LIGHT = 'light'  # Легкая активность (1-3 тренировки в неделю)
    MODERATE = 'moderate'  # Средняя активность (3-5 тренировок в неделю)
    ACTIVE = 'active'  # Высокая активность (6-7 тренировок в неделю)
    ATHLETE = 'athlete'  # Спортсмен


class UserActivity(Base):
    '''Активность пользователя'''
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    activity_level = Column(Enum(ActivityLevel), nullable=False)

    user = relationship('User', back_populates='activity')


class UserGoals(enum.Enum):
    '''Цели пользователя'''
    LOSE_WEIGHT = 'lose weight' # похудение
    KEEPING_FIT = 'keeping fit' # поддержание формы
    GAIN_MUSCLE_MASS = 'gain muscle mass' # набрать мышечную массу


class UserGoal(Base):
    '''История целей пользователя'''
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    goal = Column(Enum(UserGoals), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  

    user = relationship('User', back_populates='goal')

