from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    API_PREFIX: str
    GEMINI_API_KEY: str
    MONGODB_URL: str
    DATABASE_NAME: str
    
    class Config:
        env_file = ".env"


settings = Settings()