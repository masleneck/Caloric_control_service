from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.db import Base

class Role(enum.Enum):
    '''Роли'''
    USER = 'user'
    ADMIN = 'admin'

class User(Base):
    '''Хранит информацию для авторизации'''
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(
        default = Role.USER, # Этот параметр задает значение по умолчанию на уровне приложения (SQLAlchemy)
        server_default = text("'user'") # Этот параметр задает значение по умолчанию на уровне базы данных
    )



