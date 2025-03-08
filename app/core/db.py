from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, class_mapper
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from app.core.config import settings


DATABASE_URL =settings.database_url
# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(url=DATABASE_URL) 
# Создаем фабрику сессий для взаимодействия с базой данных
new_session = async_sessionmaker(engine, expire_on_commit=False) 


def connection(method): # принимает исходную функцию для обёртки
    async def wrapper(*args, **kwargs): # это функция-обёртка, которая принимает все аргументы исходной функции
        async with new_session() as session:
    # автоматически создаёт и закрывает сессию в асинхронном режиме, освобождая от управления сессией вручную
    # Сессия передаётся в исходную функцию через аргумент session
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper



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
    
    
    def to_dict(self) -> dict:
        '''Универсальный метод для конвертации объекта SQLAlchemy в словарь
        class_mapper(self.__class__) — этот метод возвращает объект маппера SQLAlchemy, который содержит информацию о всех колонках модели.

        {column.key: getattr(self, column.key)} — создает словарь, в котором ключи — это названия колонок,
        а значения — данные этих колонок для текущего объекта.

        Этот метод универсален и будет работать с любой таблицей или моделью, унаследованной от класса Base.
        '''
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}
    


