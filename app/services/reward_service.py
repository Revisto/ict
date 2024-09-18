# app/services/reward_service.py
import json
from app.models import User, Campaign, UserCampaignScore, Game
from app.services.coupon_service import handle_coupon_generation
from app import db

def handle_game_reward(campaign_id, game, user_id=None):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {'message': 'Campaign not found'}

    if campaign.campaign_type == 'coupon':
        return handle_coupon_generation(campaign_id)

    elif campaign.campaign_type == 'score' and user_id:
        user = User.query.get(user_id)
        user_score = UserCampaignScore.query.filter_by(user_id=user_id, campaign_id=campaign_id).first()
        if not user_score:
            user_score = UserCampaignScore(user_id=user_id, campaign_id=campaign_id, score=0)
            db.session.add(user_score)

        if not user:
            return {'message': 'User not found'}

        if not game:
            return {'message': 'Game not found'}

        user_score.score += game.score_increment
        db.session.commit()
        return {'message': 'Score updated', 'score': user_score.score}
    
    return {'message': 'Invalid campaign type or user not logged in'}