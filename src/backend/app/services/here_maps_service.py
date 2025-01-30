"""
HERE Maps service for traffic and routing data
"""
import httpx
import logging
from fastapi import HTTPException
from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class HereMapsService:
    """Service for interacting with HERE Maps APIs"""
    
    def __init__(self):
        """Initialize HERE Maps service"""
        self.api_key = settings.HERE_API_KEY
        self.base_url = "https://router.hereapi.com/v8"
    
    async def get_traffic_flow(self, bbox: tuple):
        """Get traffic flow data within bounding box"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/flow",
                    params={
                        "apiKey": self.api_key,
                        "bbox": f"{bbox[0]},{bbox[1]};{bbox[2]},{bbox[3]}",
                        "responseattributes": "sh,fc",
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching traffic data: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error fetching traffic data"
            )
    
    async def calculate_route(self, start: tuple, end: tuple):
        """Calculate optimal route between two points"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/routes",
                    params={
                        "apiKey": self.api_key,
                        "origin": f"{start[0]},{start[1]}",
                        "destination": f"{end[0]},{end[1]}",
                        "return": "summary,polyline,actions,instructions",
                        "transportMode": "car",
                        "traffic": "enabled"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error calculating route: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error calculating route"
            ) 