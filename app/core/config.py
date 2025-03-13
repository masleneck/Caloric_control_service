from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_TITLE : str = 'APP_TITLE'
    DATABASE_URL: str = 'DATABASE_URL'
    SECRET_KEY: str = 'SECRET_KEY'
    ALGORITHM: str = 'ALGORITHM'

    class Config:
        env_file = '.env'

settings = Settings()