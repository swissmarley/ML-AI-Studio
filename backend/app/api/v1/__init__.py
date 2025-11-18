"""API v1 routes"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, projects, datasets, models, ai_tools, visualization

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(ai_tools.router, prefix="/ai-tools", tags=["ai-tools"])
api_router.include_router(visualization.router, prefix="/visualization", tags=["visualization"])

