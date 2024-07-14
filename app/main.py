from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.routes import router

settings = Settings()


def get_app() -> FastAPI:
    """
    Create FastAPI app with specified settings
    """
    app = FastAPI(**settings.fastapi_kwargs)
    # Mount CSS
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
    # Add routes
    app.include_router(router)

    return app


app = get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
