from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.data.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    text: Mapped[str]
    type: Mapped[str]  # 'options' или 'input'
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)