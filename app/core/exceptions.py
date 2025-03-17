from fastapi import HTTPException, status


class AppException(HTTPException):
    '''Базовый класс для всех ошибок приложения'''
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)


# === Ошибки, связанные с пользователем ===
class UserAlreadyExistsException(AppException):
    '''Ошибка: пользователь уже существует'''
    def __init__(self):
        super().__init__('Пользователь уже существует', status.HTTP_409_CONFLICT)


class UserNotFoundException(AppException):
    '''Ошибка: пользователь не найден'''
    def __init__(self):
        super().__init__('Пользователь не найден', status.HTTP_404_NOT_FOUND)


class UserIdNotFoundException(AppException):
    '''Ошибка: отсутствует идентификатор пользователя'''
    def __init__(self):
        super().__init__('Отсутствует идентификатор пользователя', status.HTTP_404_NOT_FOUND)


# === Ошибки авторизации ===
class IncorrectEmailOrPasswordException(AppException):
    '''Ошибка: неверная почта или пароль'''
    def __init__(self):
        super().__init__('Неверная почта или пароль', status.HTTP_400_BAD_REQUEST)


class TokenExpiredException(AppException):
    '''Ошибка: токен истек'''
    def __init__(self):
        super().__init__('Токен истек', status.HTTP_401_UNAUTHORIZED)


class InvalidTokenFormatException(AppException):
    '''Ошибка: некорректный формат токена'''
    def __init__(self):
        super().__init__('Некорректный формат токена', status.HTTP_400_BAD_REQUEST)


class TokenNotFoundException(AppException):
    '''Ошибка: токен отсутствует в заголовке'''
    def __init__(self):
        super().__init__('Токен отсутствует в заголовке', status.HTTP_400_BAD_REQUEST)


class InvalidJwtTokenException(AppException):
    '''Ошибка: невалидный JWT-токен'''
    def __init__(self):
        super().__init__('Токен не валидный', status.HTTP_401_UNAUTHORIZED)


# === Ошибки доступа ===
class ForbiddenException(AppException):
    '''Ошибка: недостаточно прав'''
    def __init__(self):
        super().__init__('Недостаточно прав', status.HTTP_403_FORBIDDEN)


class TokenInvalidFormatException(AppException):
    '''Ошибка: неверный формат токена. Ожидается 'Bearer <токен>'''
    def __init__(self):
        super().__init__('Неверный формат токена. Ожидается "Bearer <токен>"', status.HTTP_400_BAD_REQUEST)

        
# === Ошибки nutrition ===
class MealNotFound(HTTPException):
    '''Ошибка: прием пищи не найден.'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class NutritionalInfoNotFound(HTTPException):
    '''Ошибка: информация о питании не найдена.'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class InvalidQuantity(HTTPException):
    '''Ошибка: недопустимое количество продукта.'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class FoodItemNotFound(HTTPException):
    '''Ошибка: продукт не найден.'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class MealAlreadyExists(HTTPException):
    '''Ошибка: прием пищи уже существует.'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )