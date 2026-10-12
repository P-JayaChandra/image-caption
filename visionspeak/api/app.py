"""
VisionSpeak FastAPI Application Factory
=======================================
Configures FastAPI instance with CORS, global exception logging,
and graceful resource management.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from visionspeak.config import get_config
from visionspeak.api.routes import router
from visionspeak.storage.database import init_db
from visionspeak.models.manager import get_model_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle context manager: initializes database and cleans up resources on exit."""
    # Startup actions
    config = get_config()
    config.ensure_directories()
    init_db()
    
    yield

    # Shutdown actions
    model_mgr = get_model_manager()
    model_mgr.unload_model()

def create_app() -> FastAPI:
    """Build and configure the VisionSpeak FastAPI application."""
    config = get_config()

    app = FastAPI(
        title="VisionSpeak AI",
        description="High-Performance Local AI Image Captioning Platform powered by Salesforce BLIP",
        version="1.0.0",
        lifespan=lifespan
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(exc),
                "type": type(exc).__name__,
                "path": str(request.url.path)
            }
        )

    # Mount API routes
    app.include_router(router)

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": "VisionSpeak AI Platform",
            "version": "1.0.0",
            "mode": "Local AI (Salesforce BLIP)",
            "documentation": "/docs",
            "health": "/api/health"
        }

    return app

# Application instance for ASGI runners (uvicorn visionspeak.api.app:app)
app = create_app()
