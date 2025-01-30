"""
Smart Traffic AI - Backend API
Main application file
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import traffic
from .config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="Real-time traffic analysis and prediction system",
    version=settings.APP_VERSION
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(
    traffic.router,
    prefix=f"{settings.API_V1_PREFIX}/traffic",
    tags=["traffic"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": settings.APP_NAME,
        "status": "active",
        "version": settings.APP_VERSION
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "cache": "connected",
            "external_apis": {
                "osm": "connected",
                "here_maps": "connected",
                "weather": "connected"
            }
        }
    } 