# src/decisionengine/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    # Mongo
    MONGO_URI: str = Field(..., description="Connection string de MongoDB Atlas")
    MONGO_DB: str = Field(default="decision_engine", description="Nombre de la base de datos a usar")

    # Auth/JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  

    # Lectura de .env
    model_config = ConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()