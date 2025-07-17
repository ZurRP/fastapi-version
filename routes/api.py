# routes/api.py
from fastapi import APIRouter
from db import SessionLocal
from models import Game

router = APIRouter(prefix="/api")

@router.get("/games")
def get_games():
    session = SessionLocal()
    try:
        games = session.query(Game.name).all()
        return [g[0] for g in games]  # מחזיר רק את שמות המשחקים
    finally:
        session.close()


@router.get("/health")
def health_check():
    return {"status": "ok"}
