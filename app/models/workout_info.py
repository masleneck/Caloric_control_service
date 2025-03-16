from sqlalchemy.orm import Mapped, relationship

from app.data.db import Base


class WorkoutInfo(Base):
    '''Хранит информацию о тренировках'''
    __tablename__ = 'workout_info'

    name: Mapped[str]
    duration_minutes: Mapped[int]
    calories_burned: Mapped[float]
    description: Mapped[str | None]

    # Связь один-ко-многим с Workout
    workouts: Mapped[list['Workout']] = relationship(
        'Workout',
        back_populates='workout_info',
        cascade="all, delete-orphan"  
    )

  