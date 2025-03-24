from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"
    SQL_ECHO: bool = True
    
    # API配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Travel Recommendation System"
    
    # Qwen API配置
    QWEN_API_URL: str = "http://103.237.29.236:10069/de_learning/v1"
    QWEN_MODEL_NAME: str = "Qwen/Qwen2.5-7B-Instruct"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # 环境配置
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    class Config:
        case_sensitive = True

settings = Settings() 