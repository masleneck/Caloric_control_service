from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class UserWorkout(Base):
    '''Связь пользователей и их тренировок'''
    __tablename__ = 'user_workouts'

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default = func.now(),
    )  
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"), 
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    


