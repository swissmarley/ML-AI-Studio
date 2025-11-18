"""
ML-AI Studio Backend
FastAPI application serving the ML/AI Studio platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="ML-AI Studio API",
    description="Comprehensive Machine Learning and AI Studio Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse({
        "message": "ML-AI Studio API",
        "version": "1.0.0",
        "docs": "/docs"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from app.core.database import engine
    from sqlalchemy import text
    
    db_status = "unknown"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JSONResponse({
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "ml-ai-studio-backend",
        "database": db_status
    })


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

