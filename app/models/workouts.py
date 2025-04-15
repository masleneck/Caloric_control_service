from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.core.database import Base

class Workout(Base):
    '''Хранит информацию о тренировках'''
    __tablename__ = 'workouts'

    name: Mapped[str] = mapped_column(
        String(100),
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
    )
    calories_burned: Mapped[float] = mapped_column(
        Float,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    # Связь многие-ко-многим с Users через UserWorkout
    users: Mapped[list["User"]]= relationship(
        back_populates="workouts",
        secondary="user_workouts", # название таблицы, через которую связы
        lazy="selectin",
        viewonly=True
    )