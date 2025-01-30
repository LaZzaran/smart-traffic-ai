"""
Traffic and routing endpoints
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Tuple
from ...services.osm_service import OpenStreetMapService
from ...services.here_maps_service import HereMapsService
from ...services.weather_service import WeatherService

router = APIRouter()

@router.get("/traffic/flow")
async def get_traffic_flow(
    bbox: Tuple[float, float, float, float] = Query(..., description="Bounding box coordinates (min_lat, min_lon, max_lat, max_lon)"),
    here_maps: HereMapsService = Depends(HereMapsService),
):
    """Get traffic flow data for a specific area"""
    return await here_maps.get_traffic_flow(bbox)

@router.get("/route/optimize")
async def optimize_route(
    start_lat: float = Query(..., description="Starting point latitude"),
    start_lon: float = Query(..., description="Starting point longitude"),
    end_lat: float = Query(..., description="Ending point latitude"),
    end_lon: float = Query(..., description="Ending point longitude"),
    here_maps: HereMapsService = Depends(HereMapsService),
    weather: WeatherService = Depends(WeatherService),
):
    """Get optimized route with traffic and weather conditions"""
    # Get route data
    route_data = await here_maps.calculate_route(
        (start_lat, start_lon),
        (end_lat, end_lon)
    )
    
    # Get weather data for destination
    weather_data = await weather.get_current_weather(end_lat, end_lon)
    
    return {
        "route": route_data,
        "weather": weather_data
    }

@router.get("/map/roads")
async def get_road_data(
    bbox: Tuple[float, float, float, float] = Query(..., description="Bounding box coordinates (min_lat, min_lon, max_lat, max_lon)"),
    osm: OpenStreetMapService = Depends(OpenStreetMapService),
):
    """Get road network data for a specific area"""
    return await osm.get_road_data(bbox) 