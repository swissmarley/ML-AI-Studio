"""Application configuration"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "ML-AI Studio"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Database
    DATABASE_URL: str = "postgresql://mlai_user:mlai_password@localhost:5432/mlai_studio"
    MONGODB_URL: str = "mongodb://mlai_user:mlai_password@localhost:27017/mlai_studio?authSource=admin"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173"
    ]
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    # File upload
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = "data/uploads"
    
    # ML/AI APIs
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    COHERE_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Jupyter
    JUPYTER_URL: str = "http://localhost:8888"
    JUPYTER_TOKEN: str = ""
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "sqlite:///mlruns.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

