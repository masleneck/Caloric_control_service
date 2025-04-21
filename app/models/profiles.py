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
    SEDENTARY = "SEDENTARY"  # Малоподвижный образ жизни < 90 минут в неделю
    LIGHT = "LIGHT"  # Легкая активность 90 < 180 минут в неделю
    MODERATE = "MODERATE"  # Средняя активность 180 < 300 минут в неделю
    ACTIVE = "ACTIVE"  # Высокая активность 300 < 480 минут в неделю
    ATHLETE = "ATHLETE"  # Спортсмен > 480 минут в неделю
    NOT_STATED= "NOT_STATED" # 0

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