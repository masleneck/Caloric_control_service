from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class User(Base):
    '''Хранит информацию для авторизации'''
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(unique=True)
    password : Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False, server_default=text('false'))

    # Связь один-к-одному с Profile
    profile: Mapped['Profile'] = relationship(  
        back_populates='user', 
        uselist=False,  # не список
        lazy='joined'  
    )

    # Связь один-к-одному с TestResult
    testresult: Mapped['TestResult'] = relationship(  
        back_populates='user', 
        uselist=False, 
        lazy='joined',
    )

    # Связь один-ко-многим с Meals
    meals: Mapped[list['Meals']] = relationship(
        back_populates='user',
        lazy='selectin',
    )
