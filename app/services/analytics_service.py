# app/services/analytics_service.py
from app.models import GameAnalytics, GeneralAnalytics
from app import db

def log_game_event(campaign_id, game_id, user_id, event_type, event_data=None):
    analytics = GameAnalytics(
        campaign_id=campaign_id,
        game_id=game_id,
        user_id=user_id,
        event_type=event_type,
        event_data=event_data
    )
    db.session.add(analytics)
    db.session.commit()

def log_general_event(campaign_id, user_id, event_type, event_data=None):
    analytics = GeneralAnalytics(
        campaign_id=campaign_id,
        user_id=user_id,
        event_type=event_type,
        event_data=event_data
    )
    db.session.add(analytics)
    db.session.commit()
