from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from fastapi.templating import Jinja2Templates
from models import Game
from db import SessionLocal
from dependencies import login_required
from utils.token_utils import generate_token, save_token

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse, name="dashboard")
async def dashboard(request: Request, auth=Depends(login_required)):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/add_game", response_class=HTMLResponse, name="add_game")
async def add_game_get(request: Request, auth=Depends(login_required)):
    return templates.TemplateResponse("add_game.html", {"request": request})


@router.post("/add_game", response_class=HTMLResponse)
async def add_game_post(
    request: Request,
    game_name: str = Form(...),
    auth=Depends(login_required)
):
    if game_name:
        session = SessionLocal()
        try:
            token = generate_token()
            new_game = Game(name=game_name, token=token)
            session.add(new_game)
            session.commit()
            save_token(game_name, token)
        finally:
            session.close()

        return templates.TemplateResponse("add_game.html", {
            "request": request,
            "token": token
        })

    return templates.TemplateResponse("add_game.html", {"request": request})


@router.get("/remove_game", response_class=HTMLResponse, name="remove_game")
async def remove_game_get(request: Request, auth=Depends(login_required)):
    session = SessionLocal()
    try:
        games = session.query(Game).all()
        return templates.TemplateResponse("remove_game.html", {
            "request": request,
            "games": games
        })
    finally:
        session.close()


@router.post("/remove_game", response_class=HTMLResponse)
async def remove_game_post(
    request: Request,
    game_name: str = Form(...),
    auth=Depends(login_required)
):
    session = SessionLocal()
    try:
        game = session.query(Game).filter_by(name=game_name).first()
        if game:
            session.delete(game)
            session.commit()
    finally:
        session.close()

    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
