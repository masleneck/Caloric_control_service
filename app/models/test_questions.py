from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    __tablename__ = "test_questions"

    name: Mapped[str] 
    text: Mapped[str]
    type: Mapped[str]  # 'options' или 'input'
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)