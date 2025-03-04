from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    __tablename__ = 'test_questions'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)  
    type = Column(String, nullable=False)  # 'options' или 'input'
    options = Column(String, nullable=True)  

    test_results = relationship('TestResult', back_populates='question', cascade='all, delete-orphan')
