from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from dependencies import login_required
from db import SessionLocal
from models import Game
from .data_helpers import get_game_data
from routes.metrics_helpers import calculate_game_metrics
from utils.token_utils import get_token

router = APIRouter(prefix="/api/data")


@router.get("/all")
async def get_all_games_data(auth=Depends(login_required)):
    def fetch_all():
        session = SessionLocal()
        try:
            games = session.query(Game).all()
            aggregated_data = {
                'ViewsTotal': 0,
                'TimesTotal': 0,
                'TotalDurationReadable': '',
                'TimeAverage': 0,
                'EngagementTotal': 0,
                'Retention': 0,
                'actions': []
            }

            total_sessions = 0
            total_durations = 0

            for game in games:
                game_data = get_game_data(game, session)
                aggregated_data['ViewsTotal'] += game_data['ViewsTotal']
                aggregated_data['TimesTotal'] += game_data['TimesTotal']
                aggregated_data['EngagementTotal'] += game_data['EngagementTotal']
                aggregated_data['Retention'] += game_data['Retention']
                aggregated_data['actions'].extend(game_data['actions'])

                total_sessions += game_data['Sessions']
                total_durations += game_data['TimesTotal']

            aggregated_data['TimeAverage'] = (
                total_durations / total_sessions if total_sessions else 0
            )
            aggregated_data['Retention'] = (
                aggregated_data['Retention'] / len(games) if games else 0
            )

            total_seconds = aggregated_data['TimesTotal']
            h, rem = divmod(int(total_seconds), 3600)
            m, s = divmod(rem, 60)
            aggregated_data['TotalDurationReadable'] = f"{h}h {m}m {s}s"

            return aggregated_data
        finally:
            session.close()

    result = await run_in_threadpool(fetch_all)
    return JSONResponse(content=result)


@router.get("/metrics/{game_name}")
async def get_metrics_for_game(game_name: str, auth=Depends(login_required)):
    def fetch_metrics():
        session = SessionLocal()
        try:
            token = get_token(game_name)
            game = session.query(Game).filter_by(name=game_name, token=token).first()
            if not game:
                return None
            metrics = calculate_game_metrics(game, session)
            return metrics
        finally:
            session.close()

    metrics = await run_in_threadpool(fetch_metrics)
    if metrics is None:
        return JSONResponse(status_code=404, content={"message": "Invalid token or game not found"})
    return JSONResponse(content=metrics)


@router.get("/games")
async def get_games(auth=Depends(login_required)):
    def fetch_games():
        session = SessionLocal()
        try:
            games = session.query(Game).all()
            return [g.name for g in games]
        finally:
            session.close()

    games = await run_in_threadpool(fetch_games)
    return games


@router.get("/{game_name}")
async def get_game_data_api(game_name: str, limit: int = 100, offset: int = 0, auth=Depends(login_required)):
    def fetch_data():
        session = SessionLocal()
        try:
            token = get_token(game_name)
            game = session.query(Game).filter_by(name=game_name, token=token).first()
            if not game:
                return None
            return get_game_data(game, session, limit=limit, offset=offset)
        finally:
            session.close()

    data = await run_in_threadpool(fetch_data)
    if data is None:
        return JSONResponse(status_code=404, content={"message": "Game not found or invalid token"})
    return JSONResponse(content=data)
