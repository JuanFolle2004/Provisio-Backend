from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv(dotenv_path=".env")


class Settings(BaseSettings):
    DATABASE_URL: str
    PORT: int = 8000

    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()
