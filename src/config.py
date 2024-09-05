import logging
from pathlib import Path
from typing import Any

from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    APP_DIR: Path = APP_DIR

    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATE_DIR: Path = APP_DIR / "templates"

    DATA_DIR: Path = APP_DIR.parent / "data"
    RAW_DATA: str = "data.json"
    DATABASE: str = "_db.json"

    FASTAPI_PROPERTIES: dict[str, Any] = {
        "title": "Gigsgo.at",
        "description": "Live music listings",
        "version": "0.0.1",
        "default_response_class": HTMLResponse,  # Override default JSONResponse
    }

    DISABLE_DOCS: bool = True

    LOG_DIR: Path = APP_DIR.parent / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE: str = str(LOG_DIR / "app.log")
    LOG_LEVEL: str = "DEBUG"

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        """
        Creates dict of values to pass to FastAPI app as **kwargs

        Returns
        -------
        fastapi_kwargs : dict
            Can be unpacked as **kwargs to pass to FastAPI app.
        """
        fastapi_kwargs = self.FASTAPI_PROPERTIES
        if self.DISABLE_DOCS:
            fastapi_kwargs.update(
                {
                    "openapi_url": None,
                    "openapi_prefix": None,
                    "docs_url": None,
                    "redoc_url": None,
                }
            )
        return fastapi_kwargs

    def setup_logging(self):
        """Creates a logger with default settings"""
        logging.basicConfig(
            filename=self.LOG_FILE,
            level=getattr(logging, self.LOG_LEVEL.upper(), logging.INFO),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
