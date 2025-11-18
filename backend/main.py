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
    print("=" * 50)
    print("ML-AI Studio Backend Starting...")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")
    print("=" * 50)
    await init_db()
    print("Backend ready! API available at http://0.0.0.0:8000")
    print("API docs available at http://0.0.0.0:8000/docs")
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
# In development, allow all origins; in production, use configured origins
cors_origins = settings.CORS_ORIGINS
allow_creds = True
if settings.DEBUG:
    cors_origins = ["*"]  # Allow all origins in debug mode
    allow_creds = False  # Can't use credentials with wildcard origins
    print("⚠️  DEBUG MODE: CORS allows all origins")
else:
    print(f"CORS Origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_creds,
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

