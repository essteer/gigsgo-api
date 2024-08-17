from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.config import Settings
from src.crud import CRUD

settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    
    db_path = str(settings.DATA_DIR / settings.DATABASE)
    init_data_path = str(settings.DATA_DIR / settings.RAW_DATA)
    db = CRUD(db_path=db_path)
    db.init_db(init_data_path=init_data_path)
    events = db.read_all()
    
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request, 
            "events": events 
        }, 
        
    )
