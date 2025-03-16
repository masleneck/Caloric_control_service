from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import JSON
from app.data.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    text: Mapped[str]  
    type: Mapped[str]  # 'options' или 'input'
    options: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    
    # Связь один-к-одному с TestResult
    testresult: Mapped['TestResult'] = relationship(  
    'TestResult',
    back_populates='testquestion',
    uselist=False,  
    lazy='joined'  
    )

