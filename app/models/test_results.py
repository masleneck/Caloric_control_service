from datetime import datetime
from sqlalchemy import String, func, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models import Gender, CurrentGoal

class TestResult(Base):
    '''Хранит результаты тестирования до регистрации'''
    __tablename__ = "test_results"
    session_id: Mapped[str | None] = mapped_column(String(128), index=True)  # Сессия теста
    
    birthday_date: Mapped[datetime] = mapped_column(nullable=True)
    gender: Mapped[Gender] 
    goal: Mapped[CurrentGoal]
    height: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"<TestResult(session_id={self.session_id})>"
    
    # Обратная связь один-к-одному с User
    user: Mapped['User'] = relationship(
        back_populates='testresult',
        uselist=False,
        lazy='joined',
    )