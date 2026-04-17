"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import register_exception_handlers
from app.api.orders import router as orders_router


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(orders_router, prefix="/api")

    return app


app = create_app()
