from sqlalchemy import Column, Integer, ForeignKey, JSON, Float, String, Date
from sqlalchemy.orm import relationship
from datetime import date

from app.core.db import Base

class TestResult(Base):
    '''Храним информацию о результатах тестирования.'''
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    answers = Column(JSON, nullable=False)  # Храним ответы в формате JSON
    date_taken = Column(Date, default=date.today, nullable=False)  # Дата прохождения теста
    fitness_level = Column(String, nullable=True)  # Уровень физической подготовки
    recommended_calories = Column(Float, nullable=True)  # Рассчитанная дневная норма калорий

    user = relationship('User', back_populates='test_results')
