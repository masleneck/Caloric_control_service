from sqlalchemy.orm import Mapped, relationship

from app.dao.db import Base

class TestQuestion(Base):
    '''Храним вопросы для теста'''
    text: Mapped[str]  
    type: Mapped[str]  # 'options' или 'input'
    options: Mapped[str | None]
    
    # Связь один-к-одному с TestResult
    testresult: Mapped['TestResult'] = relationship(  
    'TestResult',
    back_populates='testquestion',
    uselist=False,  
    lazy='joined'  
    )

