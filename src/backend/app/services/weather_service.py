"""
OpenWeatherMap service for weather data
"""
import httpx
import logging
from fastapi import HTTPException
from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class WeatherService:
    """Service for interacting with OpenWeatherMap API"""
    
    def __init__(self):
        """Initialize weather service"""
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_URL
    
    async def get_current_weather(self, lat: float, lon: float):
        """Get current weather data for location"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error fetching weather data"
            )
    
    async def get_weather_forecast(self, lat: float, lon: float):
        """Get weather forecast for location"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching weather forecast: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error fetching weather forecast"
            ) 