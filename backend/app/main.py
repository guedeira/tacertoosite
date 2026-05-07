import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.company_routes import router as company_router
from app.routes.health_routes import router as health_router
from app.routes.validation_routes import router as validation_router


DEFAULT_CORS_ALLOWED_ORIGINS = [
    "https://tacertoosite.guedeira.dev",
]


def get_cors_allowed_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ALLOWED_ORIGINS")

    if not raw_origins:
        return DEFAULT_CORS_ALLOWED_ORIGINS

    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app() -> FastAPI:
    is_production = os.getenv("APP_ENV") == "production"

    app = FastAPI(
        title="Tá certo o site?",
        description="API para comparar dominios informados com dominios oficiais cadastrados.",
        version="1.0.0",
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_allowed_origins(),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    app.include_router(company_router)
    app.include_router(health_router)
    app.include_router(validation_router)

    return app


app = create_app()
