from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.crud.users import get_user_by_username
from app.models.users import UserRole, User
from app.core.db import get_async_session
from app.core.config import settings


# Хеширование паролей 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    '''Хеширует пароль.'''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверяет соответствие хеша и пароля.'''
    return pwd_context.verify(plain_password, hashed_password)

# Подключаем OAuth2 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


# Работа с токенами 
def create_access_token(
        data: dict, 
        expires_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes)
        ) -> str:
    '''Создает JWT-токен.'''
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> str:
    '''Проверяет токен и возвращает username.'''
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: Optional[str] = payload.get('sub')
        if not username:
            raise HTTPException(status_code=401, detail='Недействительный токен')
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail='Не удалось проверить учетные данные')

# Получение текущего пользователя 
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
        ) -> User:
    '''Возвращает текущего пользователя.'''
    username = decode_token(token)
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user


async def is_admin(
        current_user: User = Depends(get_current_user)
        ) -> User:
    '''Проверяет, является ли пользователь админом.'''
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail='Недостаточно прав')
    return current_user





'''
JWT (JSON Web Token) состоит из трёх частей, разделённых точками 
HEADER.PAYLOAD.SIGNATURE
1. HEADER (Заголовок)
Содержит информацию о типе токена и алгоритме шифрования.
{
  "alg": "HS256",
  "typ": "JWT"
}
2. PAYLOAD (Полезная нагрузка)
Содержит данные пользователя (не шифруется!).
{
  "sub": "user1", # ID или имя пользователя.
  "exp": 1708887600 #  время истечения токена (в Unix time).
}
3. SIGNATURE (Подпись)
Используется для проверки подлинности токена.
Генерируется по формуле:
HMACSHA256(
    base64UrlEncode(HEADER) + "." + base64UrlEncode(PAYLOAD),
    SECRET_KEY
)
Она защищает токен от подмены: если кто-то изменит Payload, подпись изменится.
🔥 Как работает JWT?
1️⃣ Клиент получает токен при входе в систему (POST /auth/token).
2️⃣ Отправляет токен в заголовке запроса:

Authorization: Bearer <токен>
3️⃣ Сервер проверяет подпись (SIGNATURE) и валидность (exp).
4️⃣ Если всё хорошо, сервер аутентифицирует пользователя.

Payload не зашифрован, а просто закодирован! Его можно расшифровать, но нельзя изменить без изменения подписи.

Как сервер узнаёт, что пользователь авторизован?
🔹 В каждом запросе клиент отправляет заголовок:
Authorization: Bearer <токен>
🔹 Сервер декодирует JWT (например, в get_current_user) и получает sub (имя пользователя).
🔹 Если подпись и срок действия валидны, сервер даёт доступ.
🔹 Если токен просрочен или подделан → 401 Unauthorized.
'''