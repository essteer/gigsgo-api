import subprocess
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.routes import router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI app
    Runs all code before `yield` on app startup
    Runs code after `yield` on app shutdown
    """
    try:
        subprocess.run(
            [
                "tailwindcss",
                "-i",
                f"{settings.STATIC_DIR}/src/tw.css",
                "-o",
                f"{settings.STATIC_DIR}/css/main.css",
                # "--minify"  # for production
            ]
        )
    except Exception as e:
        print(f"Error running tailwindcss: {e}")

    yield


def get_app() -> FastAPI:
    """
    Create FastAPI app with specified settings
    """
    app = FastAPI(
        lifespan=lifespan,  # for tailwind updates
        **settings.fastapi_kwargs,
    )
    # Mount CSS
    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
    # Add routes
    app.include_router(router)

    return app


app = get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
