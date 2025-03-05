from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.db import Base

class ActivityLevel(enum.Enum):
    '''Уровень активности пользователя'''
    SEDENTARY = 'sedentary'  # Малоподвижный образ жизни
    LIGHT = 'light'  # Легкая активность (1-3 тренировки в неделю)
    MODERATE = 'moderate'  # Средняя активность (3-5 тренировок в неделю)
    ACTIVE = 'active'  # Высокая активность (6-7 тренировок в неделю)
    ATHLETE = 'athlete'  # Спортсмен
    NOT_STATED= 'not stated'
    
class Activity(Base):
    '''Активность пользователя'''
    __tablename__ = 'activities'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    activity_level: Mapped[ActivityLevel] = mapped_column(default = ActivityLevel.NOT_STATED, server_default = text("'NOT_STATED'"))

    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
    'User',
    back_populates='activities',
    uselist=False
    )