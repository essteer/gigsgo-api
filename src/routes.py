from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.config import Settings

settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.get("/")
def index(request: Request):
    # return templates.TemplateResponse("main.html", {"request": requestrequest, })
    return templates.TemplateResponse(request, "main.html")
