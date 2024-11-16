import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    ALLOWED_HOSTS: list = ["*"]  # Deberías especificar los orígenes permitidos en producción
    # DATABASE_URL: str = "sqlite:///./test.db"
    redis_host: str = os.getenv("REDIS_HOST", "redis")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_db: int = int(os.getenv("REDIS_DB", 0))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    class Config:
        case_sensitive = True

settings = Settings()
