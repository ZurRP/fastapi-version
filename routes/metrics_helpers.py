from sqlalchemy.orm import Session
from models import Game, Impression, Engagement, Session as GameSession
from db import Base
from datetime import datetime




def calculate_game_metrics(game: Game, session: Session):
    impressions = session.query(Impression).filter_by(game_id=game.id).all()
    engagements = session.query(Engagement).filter_by(game_id=game.id).all()
    sessions = session.query(GameSession).filter_by(game_id=game.id).all()

    # צפיות תקינות
    views_dict = {}
    for imp in impressions:
        if imp.player_id not in views_dict:
            views_dict[imp.player_id] = 0
        if views_dict[imp.player_id] < 5:
            views_dict[imp.player_id] += 1
    views_total = sum(views_dict.values())

    # סה"כ זמן (שניות)
    total_seconds = sum(
        (s.end_time - s.start_time).total_seconds()
        for s in sessions if s.end_time
    )

    avg_time = total_seconds / len(sessions) if sessions else 0

    engagement_count = {}
    for e in engagements:
        engagement_count[e.player_id] = engagement_count.get(e.player_id, 0) + 1
    retention_ratio = len([pid for pid, count in engagement_count.items() if count > 2]) / len(engagement_count) if engagement_count else 0

    # זמן קריא
    h, rem = divmod(int(total_seconds), 3600)
    m, s = divmod(rem, 60)
    total_readable = f"{h}h {m}m {s}s"

    return {
        "ViewsTotal": views_total,
        "TimesTotal": total_seconds,
        "TimeAverage": avg_time,
        "EngagementTotal": len(engagements),
        "Retention": retention_ratio,
        "TotalDurationReadable": total_readable
    }
