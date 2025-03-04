from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base

class TestResult(Base):
    '''Хранит результаты тестирования пользователя'''
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    question_id = Column(Integer, ForeignKey('test_questions.id', ondelete='CASCADE'), nullable=False)
    answer = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='test_results')
    question = relationship('TestQuestion', back_populates='test_results')
