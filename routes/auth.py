# /routes/auth.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from starlette.middleware.sessions import SessionMiddleware

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # זה ייקח אותך לתיקיית השורש
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()

PASSWORD = "3kR9&Z7Lp$k8@Xt"  # יש להחליף לסביבה בטוחה

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, password: str = Form(...)):
    if password == PASSWORD:
        request.session["authenticated"] = True
        next_url = request.query_params.get("next", "/")
        return RedirectResponse(url=next_url, status_code=HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid password"
        })

