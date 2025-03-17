from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.responses import Response

from app.core.config import settings

def create_tokens(data: dict) -> dict:
    '''Создает access и refresh токены.'''
    now = datetime.now(timezone.utc)

    # AccessToken - 10 минут
    access_expire = now + timedelta(minutes=10)
    access_payload = data.copy()
    access_payload.update({'exp': int(access_expire.timestamp()), 'type': 'access'})
    access_token = jwt.encode(
        access_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    # RefreshToken - 7 дней
    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({'exp': int(refresh_expire.timestamp()), 'type': 'refresh'})
    refresh_token = jwt.encode(
        refresh_payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return {'access_token': access_token, 'refresh_token': refresh_token}

def set_tokens(response: Response, user_id: int):
    '''Устанавливает токены в cookies.'''
    new_tokens = create_tokens(data={'sub': str(user_id)})
    access_token = new_tokens.get('access_token')
    refresh_token = new_tokens.get('refresh_token')

    response.set_cookie(
        key='user_access_token',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax'
    )

    response.set_cookie(
        key='user_refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='lax'
    )