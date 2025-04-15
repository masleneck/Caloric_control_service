from sqlalchemy import Boolean, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT
from app.core.database import Base

class User(Base):
    '''Хранит информацию для авторизации'''
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        CITEXT(120),
        unique=True,
        index=True,
    )
    hashed_password : Mapped[str] =mapped_column(
        String(86),
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
    )

    # Связь один-к-одному с Profile
    profile: Mapped['Profile'] = relationship(  
        back_populates='user', 
        uselist=False,  # не список
        lazy='joined',
    )

    # Связь один-к-одному с TestResult
    testresult: Mapped['TestResult'] = relationship(  
        back_populates='user', 
        uselist=False, 
        lazy='joined',
    )

    # Связь один-ко-многим с Meal
    meals: Mapped[list['Meal']] = relationship(
        back_populates='user',
        lazy='selectin',
    )

    # Связь многие-ко-многим с Workout через UserWorkout
    workouts: Mapped[list["Workout"]]= relationship(
        back_populates="users",
        secondary="user_workouts", 
        lazy="selectin",
        viewonly=True, # Только для чтения, так как связь через ассоциативную таблицу
    )