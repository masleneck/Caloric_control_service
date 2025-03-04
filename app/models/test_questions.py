from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    text: Mapped[str]  
    type: Mapped[str]  # 'options' или 'input'
    options: Mapped[str | None]

