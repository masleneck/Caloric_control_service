'''
Настройка работы с базой данных (создает подключение к PostgreSQL)
Файл нужен для создания соединения с PostgreSQL и управления async сессиями SQLAlchemy

AsyncSession асинхронная версия сессии SQLAlchemy, которая позволяет работать с базой данных без блокировки

Функция get_async_session() используется в API для получения сессии
'''

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import Column, Integer 
from sqlalchemy.orm import sessionmaker, declarative_base, declared_attr

from app.core.config import settings


class PreBase:
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url, echo=True) # создает асинхронный движок для работы с базой данных. 
# echo=True включает вывод SQL-запросов в консоль, полезно для отладки


AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) # фабрика для создания сессий
# expire_on_commit=False - данные в сессии не будут удаляться после коммита (иначе после сохранения объекта к нему нельзя будет обратиться)
# class_=AsyncSession - указываем, что сессии должны быть асинхронными


async def get_async_session(): # get_db
    '''
    Генератор зависимостей для FastAPI
    '''
    async with AsyncSessionLocal() as session: # открывает сессию
        yield session # передает сессию в обработчик запроса, а после завершения автоматически закрывает ее
