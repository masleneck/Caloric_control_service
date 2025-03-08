from app.dao.base import BaseDAO
from app.models import User, Profile, Meal, FoodItem, MealFoodItem

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_profile(cls, session: AsyncSession, user_data: dict) -> User:
        """
        Добавляет пользователя и привязанный к нему профиль.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - user_data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - User - объект пользователя
        """
        # Создаем пользователя из переданных данных
        user = cls.model(
            email=user_data['email'],
            username=user_data['username'],
            hashed_password=user_data['hashed_password']
        )
        session.add(user)
        await session.flush()  # Чтобы получить user.id для профиля

        # Создаем профиль, привязанный к пользователю
        profile = Profile(
            user_id=user.id,
            name=user_data['name'], # При использовании квадратных скобок Python ожидает, что ключ существует
            gender=user_data['gender'],
            weight=user_data['weight'],
            height=user_data['height'],
            goal=user_data['goal'],
            birthday_date=user_data.get('birthday_date'), # get() обрабатывает отсутствующие ключи, возвращая None или заданное значение по умолчанию
            activity_level=user_data['activity_level']
        )
        session.add(profile)

        # Один коммит для обеих операций
        await session.commit()

        return user  # Возвращаем объект пользователя
    

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        '''
        Открытие сессии

        Формирование запроса: query = select(cls.model). На этом этапе мы только создаем SQL‑запрос. 
        Фактически это подготовленная строка, которая пока не отправлена в базу данных.

        Выполнение запроса: при помощи метода execute() мы отправляем этот запрос в базу данных и получаем ответ.

        Преобразование результата: после выполнения запроса нам нужно преобразовать результат 
        в удобный для работы формат — в данном случае это объекты модели.
        '''
        # cls - это специальный параметр в Python, который автоматически передаётся в методы класса. 
        # Он представляет собой ссылку на сам класс, где определён этот метод.

        # Создаем запрос для выборки всех пользователей
        query = select(cls.model) # SELECT * FROM users

        # Выполняем запрос и получаем результат
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.scalars().all()

        # Возвращаем список всех пользователей
        return records


    @classmethod
    async def get_username_id(cls, session: AsyncSession):
        # Создаем запрос для выборки id и username всех пользователей
        query = select(cls.model.id, cls.model.username)  # Указываем конкретные колонки
        print(query)  # Выводим запрос для отладки
        result = await session.execute(query)  # Выполняем асинхронный запрос
        records = result.all()  # Получаем все результаты
        return records  # Возвращаем список записей
    

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=data_id)
        # query = select(cls.model).filter(cls.model.id == user_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none() # точно знаем, что будет одна запись или None
        return record
    

    # Универсальный метод для получения одной записи по нескольким параметрам
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        '''
        Этот метод принимает неограниченное количество аргументов (первым всегда передаётся session) и возвращает либо одну запись, либо None. 
        Важно быть осторожным, так как если будет найдено больше одной записи, возникнет ошибка.
        '''
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record
    

    # Теперь создадим универсальный метод для получения нескольких записей:
    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        records = result.scalars().all()
        return records
    # Логика работы остаётся той же, однако мы получаем данные с помощью scalars().all(), что возвращает список объектов модели. 
    # Если фильтры не будут переданы, метод вернёт все записи из таблицы.
    # На примере книг find_one_or_none ищет определенную книгу, а find_all как поиск книг по теме или жанру, может вернуть несколько книг


class ProfileDAO(BaseDAO):
    model = Profile


class MealDAO(BaseDAO):
    model = Meal


class FoodItemDAO(BaseDAO):
    model = FoodItem


class MealFoodItemDAO(BaseDAO):
    model = MealFoodItem
