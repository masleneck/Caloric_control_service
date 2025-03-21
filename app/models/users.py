from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.data.db import Base

class Role(enum.Enum):
    '''Роли'''
    USER = 'USER'
    ADMIN = 'ADMIN'

class User(Base):
    '''Хранит информацию для авторизации'''
    email: Mapped[str] = mapped_column(unique=True)
    password : Mapped[str]
    role: Mapped[Role] = mapped_column(
        default = Role.USER, # Этот параметр задает значение по умолчанию на уровне приложения (SQLAlchemy)
        server_default = text("'USER'") # Этот параметр задает значение по умолчанию на уровне базы данных
    )

    # Связь один-к-одному с Profile
    profile: Mapped['Profile'] = relationship(  
    'Profile',
    back_populates='user', # Указывает на атрибут обратной связи в модели Profile. 
    # Это значит, что при доступе к профилю можно также получить связанного пользователя.
    uselist=False  # Ключевой параметр для связи один-к-одному
    )

    # Связь один-к-одному с TestResult
    testresult: Mapped['TestResult'] = relationship(  
    'TestResult',
    back_populates='user', 
    uselist=False, 
    )

    # Связь один-ко-многим с Meal
    meals: Mapped[list['Meal']] = relationship(
        'Meal',
        back_populates='user',
        cascade="all, delete-orphan",  # При удалении User удаляются и связанные Post
    )

    # Связь один-ко-многим с Workout
    workouts: Mapped[list['Workout']] = relationship(
        'Workout',
        back_populates='user',
        cascade="all, delete-orphan"  # При удалении User удаляются и связанные Workout
    )

