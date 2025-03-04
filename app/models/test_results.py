from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

class TestResult(Base):
    '''Хранит результаты тестирования пользователя'''
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('testquestions.id'))
    answer: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default = func.now())  

