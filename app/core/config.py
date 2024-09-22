from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    ALLOWED_HOSTS: list = ["*"]  # Deberías especificar los orígenes permitidos en producción
    # DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        case_sensitive = True

settings = Settings()
