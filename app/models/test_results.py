from datetime import date, datetime
import uuid
from sqlalchemy import Date, DateTime, Float, Integer, func, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import Gender, CurrentGoal

class TestResult(Base):
    '''Хранит результаты тестирования до регистрации'''
    __tablename__ = "test_results"
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), 
    )  # Сессия теста
    
    birthday_date: Mapped[date] = mapped_column(
        Date,
    )
    gender: Mapped[Gender]
    goal: Mapped[CurrentGoal]
    height: Mapped[float] = mapped_column(
        Float,
    )
    weight: Mapped[float] = mapped_column(
        Float,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete="SET NULL"),
        unique=True,
    )

    def __repr__(self):
        return f"<TestResult(session_id={self.session_id})>"
    
    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
        back_populates='testresult',
        uselist=False,
        lazy='joined',
    )