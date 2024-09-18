# app/services/reward_service.py
import json
from app.models import User, Campaign
from app.services.coupon_service import handle_coupon_generation
from app import db

def load_game_rewards():
    with open('app/config/game_rewards.json') as f:
        return json.load(f)

game_rewards = load_game_rewards()

def handle_game_reward(campaign_id, game_name, user_id=None):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        return {'message': 'Campaign not found'}

    if campaign.campaign_type == 'coupon':
        return handle_coupon_generation(campaign_id)

    elif campaign.campaign_type == 'score' and user_id:
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}

        score_increment = game_rewards.get(game_name, {}).get('score_increment', 10)
        user.score += score_increment
        db.session.commit()
        return {'message': 'Score updated', 'score': user.score}
    
    return {'message': 'Invalid campaign type or user not logged in'}