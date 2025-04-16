from datetime import date
from sqlalchemy import Date, Float, ForeignKey, Index, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class UserWorkout(Base):
    '''Связь пользователей и их тренировок'''
    __tablename__ = 'user_workouts'

    workout_date: Mapped[date] = mapped_column(
        Date,
        server_default = func.current_date(),
        index=True,
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
    )
    calories_burned: Mapped[float] = mapped_column(
        Float,
    )  
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"), 
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    
    __table_args__ = (
        # Составной индекс для часто используемых запросов
        Index(
            'ix_user_workouts_user_date',
            user_id,
            workout_date
        ),
    )
