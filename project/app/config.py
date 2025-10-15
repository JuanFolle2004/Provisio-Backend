from pydantic_settings import BaseSettings
import firebase_admin
from firebase_admin import credentials


class Settings(BaseSettings):
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_DB_URL: str
    DATABASE_URL: str = "postgresql://localhost:5432/postgres"
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()


def init_firebase():
    if not firebase_admin._apps:
        private_key = settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n')

        cred_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": private_key,
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
        }

        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.FIREBASE_DB_URL
        })
