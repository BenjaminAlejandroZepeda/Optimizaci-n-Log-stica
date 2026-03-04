from fastapi import FastAPI
from decisionengine.api.v1.routes import router as router
from decisionengine.api.errors import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="Decision Engine")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api/v1")

    register_exception_handlers(app)

    return app


app = create_app()