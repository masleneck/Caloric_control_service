from typing import List, Any, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    '''
    Базовый класс для работы с базой данных, который предоставляет универсальные методы для добавления данных в таблицы.
    Он использует SQLAlchemy для взаимодействия с базой данных в асинхронном режиме.

    Атрибут model: Это переменная, которая будет установлена в дочернем классе.
    В дочерних классах будет указана конкретная модель базы данных (например, User, Profile и т. д.), с которой будет работать этот класс. 
    Благодаря этой переменной мы сможем гибко создавать дочерние классы, внутри которых уже будем добавлять конкретную модель. 
    Этот подход позволяет как легко использовать универсальные методы базового класса, так и позволяет описывать собственные методы 

    Метод add: Этот метод позволяет добавить одну запись (например, одного пользователя) в базу данных.

    Он принимает сессию базы данных и значения для полей записи в виде именованных аргументов (**values).

    Создаётся новый экземпляр модели с переданными данными, затем он добавляется в сессию.

    После этого вызывается commit, чтобы зафиксировать изменения в базе данных.

    В случае ошибки, происходит откат (rollback), и ошибка выбрасывается.

    Метод add_many: Этот метод используется для добавления сразу нескольких записей в базу данных за один раз.

    Он принимает список словарей, где каждый словарь содержит данные для одной записи.

    Из этих словарей создаются экземпляры модели и добавляются в сессию с помощью add_all.

    После добавления всех экземпляров вызывается коммит для сохранения изменений.

    Если возникает ошибка, как и в первом методе, вызывается откат транзакции и ошибка поднимается дальше.
    '''
    model = None  # Устанавливается в дочернем классе

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances