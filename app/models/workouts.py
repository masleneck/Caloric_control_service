from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db import Base


class Workout(Base):
    '''Связь пользователей и их тренировок'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    workout_info_id: Mapped[int] = mapped_column(ForeignKey('workout_info.id'))
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())  

    # Связь многие-к-одному с User
    user: Mapped['User'] = relationship(
        'User',
        back_populates='workouts'
    )

    # Связь многие-к-одному с WorkoutInfo
    workout_info: Mapped['WorkoutInfo'] = relationship(
        'WorkoutInfo',
        back_populates='workouts'
    )



