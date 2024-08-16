from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.config import Settings
from src.crud import CRUD

settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    
    db = CRUD(db_path=str(settings.DATA_DIR / settings.DATABASE))
    events = db.all_items()
    
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request, 
            "events": events 
        }, 
        
    )
