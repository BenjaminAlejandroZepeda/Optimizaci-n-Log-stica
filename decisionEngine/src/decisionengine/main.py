from fastapi import FastAPI
from decisionengine.api.v1.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Decision Engine")

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
