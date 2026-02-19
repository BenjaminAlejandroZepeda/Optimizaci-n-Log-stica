from fastapi import FastAPI
from decisionengine.api.v1.routes import router as api_router
from decisionengine.api.errors import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Decision Engine")
    app.include_router(api_router, prefix="/api/v1")

    register_exception_handlers(app)

    return app


app = create_app()
