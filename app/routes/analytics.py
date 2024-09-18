# app/routes/analytics.py
from flask import Blueprint, jsonify, render_template
from app.models import Campaign, CampaignGame, GameAnalytics, GeneralAnalytics, Game

bp = Blueprint('analytics', __name__)

@bp.route('/analytics/game/<int:campaign_id>/<int:game_id>', methods=['GET'])
def get_game_analytics(campaign_id, game_id):
    analytics = GameAnalytics.query.filter_by(campaign_id=campaign_id, game_id=game_id).all()
    return jsonify([a.to_dict() for a in analytics])

@bp.route('/analytics/general/<int:campaign_id>', methods=['GET'])
def get_general_analytics(campaign_id):
    analytics = GeneralAnalytics.query.filter_by(campaign_id=campaign_id).all()
    return jsonify([a.to_dict() for a in analytics])

@bp.route('/analytics/dashboard/<int:campaign_id>/<int:game_id>', methods=['GET'])
def analytics_dashboard(campaign_id, game_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    game = Game.query.get_or_404(game_id)
    return render_template('analytics_dashboard.html', campaign=campaign, game=game)

@bp.route('/analytics', methods=['GET'])
def main_analytics_dashboard():
    campaigns = Campaign.query.all()
    campaign_games = {campaign.id: CampaignGame.query.filter_by(campaign_id=campaign.id).all() for campaign in campaigns}
    return render_template('main_analytics_dashboard.html', campaigns=campaigns, campaign_games=campaign_games)