from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.db import Base

class Gender(enum.Enum):
    '''Пол пользователя'''
    MALE = 'male'
    FEMALE = 'female'
    NOT_STATED = 'not stated'

class Profile(Base):
    '''Хранит информацию пользователя'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    gender: Mapped[Gender] = mapped_column(default = Gender.NOT_STATED, server_default = text("'NOT_STATED'"))
    weight: Mapped[float]
    height: Mapped[int]
    birthday_date: Mapped[datetime | None] = mapped_column(DateTime)
    
    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
    'User',
    back_populates='profile',
    uselist=False
    )