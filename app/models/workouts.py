from sqlalchemy import Index, String, Text, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.core.database import Base

class Workout(Base):
    '''Хранит информацию о тренировках'''
    __tablename__ = 'workouts'

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    __table_args__ = (
        # Основной триграммный индекс для нечеткого поиска
        Index(
            'ix_workouts_name_trgm', 
            name, 
            postgresql_using='gin',
            postgresql_ops={'name': 'gin_trgm_ops'}
        ),
        
        # Индекс для регистронезависимого поиска
        Index(
            'ix_workouts_name_lower',
            func.lower(name),
            postgresql_using='btree'
        ),
        
        # Составной индекс для часто используемых запросов
        Index(
            'ix_workouts_name_description_trgm',
            name,
            description,
            postgresql_using='gin',
            postgresql_ops={
                'name': 'gin_trgm_ops',
                'description': 'gin_trgm_ops'
            }
        ),
    )
    
    # Связь многие-ко-многим с Users через UserWorkout
    users: Mapped[list["User"]]= relationship(
        back_populates="workouts",
        secondary="user_workouts", # название таблицы, через которую связы
        lazy="selectin",
        viewonly=True
    )