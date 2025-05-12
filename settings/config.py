from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ROOT_PATH: Path = Path(__file__).parent.parent
    MEDIA_PATH: Path = ROOT_PATH / 'static' / 'media'
    
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # В продакшене заменить на безопасный ключ
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней

    # database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    DATABASE_SQLITE: str = "sqlite:///main.db"
    
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env", env_file_encoding="utf-8"
    )

    def get_db_url(self, asyncio=False, lite=False):
        if lite:
            return self.DATABASE_SQLITE
        if asyncio:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
