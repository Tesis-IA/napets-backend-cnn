from typing import Optional, Union
import os
from functools import lru_cache


class Settings:
    PROJECT_NAME: Optional[str] = os.getenv('PROJECT_NAME')
    PROJECT_VERSION: Optional[str] = os.getenv('PROJECT_VERSION', '1.0.0')
    POSTGRES_USER: Optional[str] = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: Optional[str] = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: Optional[str] = os.getenv('POSTGRES_SERVER', 'localhost')
    POSTGRES_PORT: Union[str, int, None] = os.getenv('POSTGRES_PORT', 5432)
    POSTGRES_DB: Optional[str] = os.getenv('POSTGRES_DB', 'tdd')
    ML_MODEL: Optional[str] = os.getenv('ML_MODEL', 'model')
    ENVIRONMENT: Optional[str] = os.getenv('ENVIRONMENT', 'test')
    DATABASE_URL: str = ''
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'somesecretkey')


@lru_cache
def get_settings() -> Settings:
    """Get cached settings."""
    settings = Settings()
    return settings
