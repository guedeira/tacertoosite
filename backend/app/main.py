import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.brand_routes import router as brand_router
from app.routes.health_routes import router as health_router
from app.routes.validation_routes import router as validation_router


CORS_ALLOWED_ORIGINS = [
    # Use esta linha apenas em desenvolvimento local.
    "*",
    # Em producao, comente a linha acima e descomente/ajuste a linha abaixo.
    # "https://SEU_USUARIO.github.io",
]


def create_app() -> FastAPI:
    is_production = os.getenv("APP_ENV") == "production"

    app = FastAPI(
        title="Validador de Dominios Oficiais",
        description="API para comparar dominios informados com dominios oficiais cadastrados.",
        version="1.0.0",
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOWED_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    app.include_router(brand_router)
    app.include_router(health_router)
    app.include_router(validation_router)

    return app


app = create_app()
