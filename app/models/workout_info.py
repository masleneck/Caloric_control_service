from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base


class WorkoutInfo(Base):
    '''Хранит информацию о тренировках'''
    __tablename__ = 'workout_info'

    name: Mapped[str]
    duration_minutes: Mapped[int]
    calories_burned: Mapped[float]
    description: Mapped[str | None]

  