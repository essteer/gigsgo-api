import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import Settings
from src.routes import router

settings = Settings()
settings.setup_logging()
logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    """
    Create FastAPI app with specified settings
    """
    try:
        
        app = FastAPI(**settings.fastapi_kwargs)
        app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
        app.include_router(router)
        logger.info("FastAPI app init OK")

        return app
    
    except Exception as e:
        logger.fatal(f"FastAPI app init error: {e}")
        raise
        


app = get_app()


if __name__ == "__main__":
    import uvicorn
    try:
        logger.info("Starting FastAPI app...")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"FastAPI app run error: {e}")
        raise
