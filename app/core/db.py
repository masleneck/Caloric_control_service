from typing import Annotated
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.core.config import settings


DATABASE_URL =settings.database_url
# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL, echo=True) 
# Создаем фабрику сессий для взаимодействия с базой данных
new_session = async_sessionmaker(engine, expire_on_commit=False) 

async def get_session():
    async with new_session() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    '''
    Base- Абстрактный базовый класс для всех моделей, от которого будут наследоваться все таблицы.
    Он не создаст отдельную таблицу в базе данных, но предоставит базовую функциональность для всех других моделей.
    DeclarativeBase: Основной класс для всех моделей, от которого будут наследоваться все таблицы (модели таблиц)
    AsyncAttrs: Позволяет создавать асинхронные модели, что улучшает производительность при работе с асинхронными операциями
    '''
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
    
