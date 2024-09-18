# app/routes/game.py
from flask import Blueprint, jsonify, request, session, redirect, url_for
from app.models import Campaign, Game, CampaignGame
from app.services.game_service import get_game_template

bp = Blueprint('game', __name__)

@bp.route('/popup/<int:campaign_id>/<int:game_id>', methods=['GET', 'POST'])
def popup(campaign_id, game_id):
    campaign_game = CampaignGame.query.filter_by(campaign_id=campaign_id, game_id=game_id).first()
    if not campaign_game:
        return jsonify({'message': 'Campaign does not have access to this game.'})

    game = Game.query.get_or_404(game_id)
    campaign = Campaign.query.get_or_404(campaign_id)

    game_template = get_game_template(game.name, campaign_id)
    if game_template:
        return game_template
    else:
        return jsonify({'message': 'Game not found.'})