from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Workout(Base):
    '''Связь пользователей и их тренировок'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    workout_info_id: Mapped[int] = mapped_column(ForeignKey('workout_info.id'))
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())  



