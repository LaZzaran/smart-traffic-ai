"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "smart_traffic"
    DATABASE_URL: str = None

    @property
    def DATABASE_URL_VALUE(self) -> str:
        """Get database URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenStreetMap (Ücretsiz)
    OSM_OVERPASS_URL: str = "https://overpass-api.de/api/interpreter"
    OSM_NOMINATIM_URL: str = "https://nominatim.openstreetmap.org"
    
    # HERE Maps (Ücretsiz API key ile)
    HERE_API_KEY: str = ""
    
    # Weather API (OpenWeatherMap - Ücretsiz tier)
    WEATHER_API_KEY: str = ""
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # Uygulama Ayarları
    APP_NAME: str = "Smart Traffic AI"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]  # Production'da değiştirilecek
    
    # Cache Settings
    CACHE_EXPIRE_TIME: int = 300  # 5 dakika
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings"""
    return Settings() 