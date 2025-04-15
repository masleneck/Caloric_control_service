from loguru import logger
from sqlalchemy import select
from fastapi import HTTPException
from app.models.profiles import Profile
from app.repositories.base import BaseDAO
from app.repositories.profile import ProfileDAO
from app.models import User,  ActivityLevel, TestResult
from app.schemas.users import UserRegister, UserAuth, UserInfo, UserCreate, ProfileCreate, UpdateConfidentialInfoRequest
from app.utils.auth_utils import get_password_hash, verify_password

class UserDAO(BaseDAO[User]):
    model = User

    async def register_user(self, user_data: UserRegister, session_id: str) -> dict:
        """Регистрация пользователя"""
        # Проверяем session_id 
        test_result = await self._session.scalar(
            select(TestResult).where(TestResult.session_id == session_id)
        )
        if not test_result:
            raise HTTPException(400, "Неверный session_id")
        # Проверяем email 
        if await self.find_one_by_fields(email=user_data.email):
            raise HTTPException(400, "Пользователь с таким email уже существует")
        # Создаём user
        user = await self.add(
            UserCreate(
                email=user_data.email,
                hashed_password=get_password_hash(user_data.password)
            )
        )
        # Создаём профиль
        profile_dao = ProfileDAO(self._session)
        await profile_dao.add( 
            ProfileCreate(
                user_id=user.id,
                name=user_data.name.capitalize(),
                last_name=user_data.last_name.capitalize() if user_data.last_name else None,
                gender=test_result.gender,
                weight=test_result.weight,
                height=test_result.height,
                goal=test_result.goal,
                birthday_date=test_result.birthday_date,
                activity_level=ActivityLevel.NOT_STATED
            )
        )
        # Удаляем TestResult
        await self._session.delete(test_result)
        await self._session.commit() 
        return {'message': 'Регистрация успешна!'}


    async def authenticate_user(self, user_data: UserAuth) -> User:
        """Аутентификация пользователя"""
        # Поиск пользователя
        user = await self.find_one_by_fields(email=user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(401, "Неверный email или пароль")
        return user


    async def update_credentials(
        self,
        user: User,
        update_data: UpdateConfidentialInfoRequest
    ) -> dict:
        """Обновление пароля"""
        # Валидация текущих данных
        if user.email != update_data.current_email or not verify_password(update_data.current_password, user.hashed_password):
            raise HTTPException(400, "Неверный email или пароль")
        # Обновление пароля (только если передан новый пароль)
        if update_data.new_password:
            user.hashed_password = get_password_hash(update_data.new_password)
        
        await self._session.commit()
        return {"message": "Данные обновлены"}
        

    async def get_all_users(
        self,
        skip: int = 0, # Пропустить N записей (по умолчанию 0)
        limit: int = 100, # Максимальное количество записей (по умолчанию 100)
        sort_by: str = 'id', # Поле для сортировки (id/email/is_superuser)
        sort_desc: bool = False # sort_desc: Сортировка по убыванию (по умолчанию False - возрастание)
    ) -> list[UserInfo]:
        """
        Получает список пользователей с пагинацией и сортировкой
        Returns: Список пользователей в формате UserInfo
        """
        # Безопасная проверка поля сортировки
        sort_field = getattr(User, sort_by, None)
        if sort_field is None:
            raise HTTPException(400, f"Недопустимое поле для сортировки: {sort_by}")
        # Определяем направление сортировки
        order_by = sort_field.desc() if sort_desc else sort_field.asc()
        # Добавляем join с профилем для полной информации
        query = (
            select(User)
            .join(Profile, User.id == Profile.user_id, isouter=True)
            .order_by(order_by)
            .offset(skip)
            .limit(limit)
        )
        users = await self._session.scalars(query)
        return [UserInfo.model_validate(u) for u in users]