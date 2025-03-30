from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_TITLE : str = 'APP_TITLE'
    DATABASE_URL: str = 'DATABASE_URL'
    SECRET_KEY: str = 'SECRET_KEY'
    ALGORITHM: str = 'ALGORITHM'
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

if __name__ == '__main__':
    print(f"APP_TITLE: {settings.APP_TITLE}")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"SECRET_KEY: {settings.SECRET_KEY}")
    print(f"ALGORITHM: {settings.ALGORITHM}")