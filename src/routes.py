import logging
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.config import Settings
from src.crud import CRUD

settings = Settings()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    try:
        db_path = str(settings.DATA_DIR / settings.DATABASE)
        init_data_path = str(settings.DATA_DIR / settings.RAW_DATA)
        
        logger.info("Initialising database")
        db = CRUD(db_path=db_path)
        db.init_db(init_data_path=init_data_path)
        
        logger.info("Reading all items from database")
        events = db.read_all()
        
        logger.info("Rendering main.html template with events")
        return templates.TemplateResponse(
            "main.html",
            {
                "request": request,
                "events": events
            }, 
        )

    except FileNotFoundError as e:
        logger.error(f"File not found during index processing: {e}")
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "Data files missing. Please contact support."
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Unexpected error in index route: {e}")
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "An unexpected error occurred. Please try again later."
            },
            status_code=500
        )


@router.get("/test-error")
def test_error(request: Request):
    try:
        raise ValueError("This is a test error!")
    except ValueError as e:
        logger.error(f"Test error: {e}")
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": "This is a simulated error for testing purposes."
            },
            status_code=500
        )
