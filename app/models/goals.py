from datetime import datetime
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.db import Base

class СurrentGoal(enum.Enum):
    '''Цели пользователя'''
    LOSE_WEIGHT = 'lose weight' # похудение
    KEEPING_FIT = 'keeping fit' # поддержание формы
    GAIN_MUSCLE_MASS = 'gain muscle mass' # набрать мышечную массу
    NOT_STATED = 'not stated'

class Goal(Base):
    '''История целей пользователя'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    goal: Mapped[СurrentGoal] = mapped_column(default = СurrentGoal.NOT_STATED, server_default = text("'NOT_STATED'"))
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())  
    
    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
    'User',
    back_populates='goal',
    uselist=False
    )

 

    