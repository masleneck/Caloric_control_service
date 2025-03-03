from sqlalchemy import Column, Integer, String, JSON

from app.core.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    __tablename__ = "test_questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)  # Текст вопроса
    type = Column(String, nullable=False)  # "options" или "input"
    options = Column(JSON, nullable=True)  # Варианты ответа (если type="options")