from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    '''Хэширует пароль.'''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверяет пароль.'''
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(user, password: str):
    '''Аутентифицирует пользователя.'''
    if not user or not verify_password(password, user.password):
        return None
    return user