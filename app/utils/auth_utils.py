from passlib.context import CryptContext
from loguru import logger

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    '''Хэширует пароль.'''
    return pwd_context.hash(password)
    


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверяет пароль.'''
    # logger.info('Проверка пароля')
    res = pwd_context.verify(plain_password, hashed_password)

    # if res:
    #     logger.info('Пароль верный')
    # else:
    #     logger.info('Пароль неверный')

    return res


async def authenticate_user(user, password: str):
    '''Аутентифицирует пользователя.'''
    if not user or not verify_password(password, user.password):
        return None
    return user

if __name__=='__main__':
    hashed = (get_password_hash('123321'))
    verify_password('123321', hashed)
    verify_password('wrongpass', hashed)