from datetime import date
from sqlalchemy import Float, ForeignKey, Date, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base

class Gender(enum.Enum):
    """Пол пользователя"""
    MALE = "MALE"
    FEMALE = "FEMALE"
    NOT_STATED = "NOT_STATED"

class CurrentGoal(enum.Enum):
    """Цели пользователя"""
    LOSE_WEIGHT = "LOSE_WEIGHT" # похудение
    KEEPING_FIT = "KEEPING_FIT" # поддержание формы
    GAIN_MUSCLE_MASS = "GAIN_MUSCLE_MASS" # набрать мышечную массу
    NOT_STATED = "NOT_STATED"

class ActivityLevel(enum.Enum):
    """Уровень активности пользователя"""
    SEDENTARY = "SEDENTARY"  # Малоподвижный образ жизни
    LIGHT = "LIGHT"  # Легкая активность (1-3 тренировки в неделю)
    MODERATE = "MODERATE"  # Средняя активность (3-5 тренировок в неделю)
    ACTIVE = "ACTIVE"  # Высокая активность (6-7 тренировок в неделю)
    ATHLETE = "ATHLETE"  # Спортсмен
    NOT_STATED= "NOT_STATED"

class Profile(Base):
    """Хранит информацию пользователя"""
    __tablename__ = "profile"

    name: Mapped[str] = mapped_column(
        String(50),
    )
    last_name: Mapped[str | None] = mapped_column(
        String(50),
    )
    gender: Mapped[Gender] = mapped_column(
        default = Gender.NOT_STATED,
        server_default = text("'NOT_STATED'"),
    )
    weight: Mapped[float] = mapped_column(
        Float,
    )
    height: Mapped[int] = mapped_column(
        Integer,
    )
    goal: Mapped[CurrentGoal] = mapped_column(
        default = CurrentGoal.NOT_STATED, 
        server_default = text("'NOT_STATED'")
    )
    birthday_date: Mapped[date | None] = mapped_column(
        Date,
    )
    activity_level: Mapped[ActivityLevel] = mapped_column(
        default = ActivityLevel.NOT_STATED,
        server_default = text("'NOT_STATED'"),
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    # Обратная связь один-к-одному с User
    user: Mapped["User"] = relationship(
        back_populates="profile",
        uselist=False,
        lazy="joined",
    )