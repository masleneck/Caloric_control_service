from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_title : str = 'APP_TITLE'
    database_url: str
    secret_key: str = 'SECRET_KEY'
    algorithm: str = 'ALGORITHM'
    access_token_expire_minutes: int 

    class Config:
        env_file = '.env'

settings = Settings()