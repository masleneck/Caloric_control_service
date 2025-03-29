from loguru import logger
from sqlalchemy import exists, select, update
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.repositories.base import BaseDAO
from app.models import User,  ActivityLevel, Profile, TestResult
from app.schemas.users import UserRegister, UserAuth, UserInfo, ConfidentialInfoResponse, UpdateConfidentialInfoRequest
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.utils.auth_utils import get_password_hash, verify_password

class UserDAO(BaseDAO[User]):
    model = User


    async def register_user(self, user_data: UserRegister, session_id: str) -> dict:
        """Регистрация пользователя"""
        try:
            # Проверяем session_id (чтение)
            test_result = await self._session.scalar(
                select(TestResult).where(TestResult.session_id == session_id)
            )
            if not test_result:
                raise HTTPException(status_code=400, detail='Неверный session_id')

            # Проверяем email (чтение)
            if await self.find_one_by_fields(email=user_data.email):
                raise UserAlreadyExistsException()

            # Основные операции записи 
            try:
                # Подготавливаем данные пользователя
                user_data_dict = user_data.model_dump(
                    exclude={'confirm_password', 'fullname'},  # Исключаем лишние поля
                    exclude_unset=True
                )
                user_data_dict['password'] = get_password_hash(user_data.password)  # Добавляем хеш пароля

                # Создаём и сохраняем пользователя
                new_user = self.model(**user_data_dict)
                self._session.add(new_user)
                await self._session.flush()  # Получаем ID

                # Создаём профиль
                profile_data = {
                    'user_id': new_user.id,
                    'name': user_data.name.capitalize(),
                    'last_name': user_data.last_name.capitalize() if user_data.last_name else None,
                    'gender': test_result.gender,
                    'weight': test_result.weight,
                    'height': test_result.height,
                    'goal': test_result.goal,
                    'birthday_date': test_result.birthday_date,
                    'activity_level': ActivityLevel.NOT_STATED,
                }
                self._session.add(Profile(**profile_data))

                # Удаляем TestResult
                await self._session.delete(test_result)

                await self._session.commit()
                return {'message': 'Регистрация успешна!'}

            except Exception as e:
                await self._session.rollback()
                logger.error(f"Ошибка при регистрации: {str(e)}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail="Произошла ошибка при регистрации"
                )

        except (HTTPException, UserAlreadyExistsException):
            raise
                


    async def authenticate_user(self, user_data: UserAuth) -> User:
        """
        Аутентификация пользователя 
        """
        try:
            # Поиск пользователя
            user = await self.find_one_by_fields(email=user_data.email)
            if not user:
                logger.warning(f"Попытка входа с несуществующим email: {user_data.email}")
                raise IncorrectEmailOrPasswordException()

            # Проверка пароля 
            if not verify_password(user_data.password, user.password):
                logger.warning(f"Неверный пароль для пользователя {user.email}")
                raise IncorrectEmailOrPasswordException()

            logger.info(f"Успешная аутентификация пользователя {user.id}")
            return user

        except IncorrectEmailOrPasswordException:
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка аутентификации: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Внутренняя ошибка сервера"
            )
 
    

    async def update_credentials(
        self,
        user: User,
        update_data: UpdateConfidentialInfoRequest
    ) -> dict:
        """Обновляет email и/или пароль пользователя в одной транзакции"""
        # Проверяем текущие данные
        if user.email != update_data.current_email or not verify_password(update_data.current_password, user.password):
            raise HTTPException(400, "Неверные текущие email или пароль")

        # Проверяем, что есть что обновлять
        if not update_data.new_email and not update_data.new_password:
            raise HTTPException(400, "Не указаны новые данные для обновления")

        # Обновляем email если нужно
        if update_data.new_email and update_data.new_email != user.email:
            if await self._session.scalar(select(exists().where(User.email == update_data.new_email, User.id != user.id))):
                raise HTTPException(400, "Новый email уже используется")
            user.email = update_data.new_email

        # Обновляем пароль если нужно
        if update_data.new_password:
            user.password = get_password_hash(update_data.new_password)

        # Сохраняем изменения
        self._session.add(user)
        await self._session.commit()

        return {"message": "Данные обновлены!"}
    


    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = 'id'
    ) -> list[UserInfo]:
        """
        Получает список пользователей с пагинацией и сортировкой
        
        Args:
            skip: Пропустить N записей
            limit: Вернуть не более N записей
            sort_by: Поле для сортировки (id/email/name)
        Returns:
            Список пользователей в формате UserInfo
        """
        # Безопасная проверка поля сортировки
        sort_field = getattr(User, sort_by, User.id)
        
        users = await self._session.scalars(
            select(User)
            .order_by(sort_field)
            .offset(skip)
            .limit(limit)
        )
        
        return [UserInfo.model_validate(u) for u in users]