from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_302_FOUND
from models import Game
from db import SessionLocal
from dependencies import login_required
from utils.package_utils import create_package
import os

router = APIRouter()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # זה ייקח אותך לתיקיית השורש
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

os.makedirs("packages", exist_ok=True)


@router.get("/package_installer", response_class=HTMLResponse)
async def package_installer_get(request: Request, auth=Depends(login_required)):
    return templates.TemplateResponse("package_installer.html", {"request": request})


@router.post("/package_installer")
async def package_installer_post(
    request: Request,
    game_name: str = Form(...),
    token: str = Form(...),
    auth=Depends(login_required)
):
    session = SessionLocal()
    try:
        game = session.query(Game).filter_by(name=game_name, token=token).first()
        if not game:
            return JSONResponse(content={"success": False, "message": "Invalid game name or token"})

        package_path = create_package(game, session)
        return JSONResponse(content={
            "success": True,
            "package_url": f"/packages/{os.path.basename(package_path)}"
        })
    finally:
        session.close()


@router.get("/packages/{filename}")
async def download_package(filename: str, auth=Depends(login_required)):
    file_path = os.path.join("packages", filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(file_path, filename=filename)
