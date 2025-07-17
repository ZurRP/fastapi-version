from sqlalchemy.orm import Session
from models import Player, Impression, Engagement, Session as GameSession, New_Ad
from datetime import datetime



def get_game_data(game, session: Session, limit: int = None, offset: int = 0):
    impressions = session.query(Impression).filter_by(game_id=game.id).all()
    engagements = session.query(Engagement).filter_by(game_id=game.id).all()
    sessions = session.query(GameSession).filter_by(game_id=game.id).all()
    ads = session.query(New_Ad).filter_by(game_id=game.id).all()
    players = session.query(Player).filter_by(game_id=game.id).all()

    # סינון אימפרשנים טובים
    filtered_impressions = [
        i for i in impressions
        if i.duration >= 2 and i.screen_percentage >= 1.5 and i.object_percentage >= 50 and i.viewing_angle >= 55
    ]

    # חישוב צפיות תקינות מול Wasted
    impressions_dict = {}
    wasted = 0
    for imp in filtered_impressions:
        if imp.player_id not in impressions_dict:
            impressions_dict[imp.player_id] = 0
        if impressions_dict[imp.player_id] < 10:
            impressions_dict[imp.player_id] += 1
        else:
            wasted += 1
    views_total = sum(impressions_dict.values())

    # זמן כולל
    total_duration = sum(
        (s.end_time - s.start_time).total_seconds()
        for s in sessions if s.end_time and s.start_time
    )
    avg_play = total_duration / len(sessions) if sessions else 0

    # ריטנשן
    engagement_count = {}
    for e in engagements:
        engagement_count[e.player_id] = engagement_count.get(e.player_id, 0) + 1

    retention_ratio = len([
        pid for pid, count in engagement_count.items() if count > 2
    ]) / len(engagement_count) if engagement_count else 0

    # יצירת פעולות לפלט
    actions = (
        [{'type': 'New Player', 'details': f"Player ID: {p.id}, Country: {p.country}, Age: {p.age}", 'timestamp': p.created_at.isoformat()} for p in players] +
        [{'type': 'Impression', 'details': f"Player ID: {i.player_id}, Ad_name: {i.ad_name}", 'timestamp': i.timestamp.isoformat()} for i in impressions] +
        [{'type': 'Engagement', 'details': f"Player ID: {e.player_id}, Type: {e.interaction_type}", 'timestamp': e.timestamp.isoformat()} for e in engagements] +
        [{'type': 'Session', 'details': f"Player ID: {s.player_id}, Start: {s.start_time}, End: {s.end_time}", 'timestamp': s.start_time.isoformat()} for s in sessions if s.start_time] +
        [{'type': 'Ad', 'details': f"Player ID: {a.player_id}, Name: {a.name}, Duration: {a.duration}", 'timestamp': a.timestamp.isoformat()} for a in ads]
    )

    # מיון לפי תאריך וחתך לפי limit/offset
    actions_sorted = sorted(actions, key=lambda x: x['timestamp'], reverse=True)
    if limit is not None:
        actions_sorted = actions_sorted[offset:offset + limit]
    else:
        actions_sorted = actions_sorted[offset:]

    return {
        "ViewsTotal": views_total,
        "TimesTotal": total_duration,
        "TimeAverage": avg_play,
        "EngagementTotal": len(engagements),
        "Retention": retention_ratio,
        "Sessions": len(sessions),
        "WastedImpressions": wasted,
        "actions": actions_sorted
    }
