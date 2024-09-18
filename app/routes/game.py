# app/routes/game.py
from flask import Blueprint, jsonify, session, redirect, url_for
from app.models import Campaign, Game, CampaignGame
from app.services.game_service import get_game_template
from app.decorators import login_required

bp = Blueprint('game', __name__)

@bp.route('/popup/<int:campaign_id>/<int:game_id>', methods=['GET', 'POST'])
def popup(campaign_id, game_id):
    campaign_game = CampaignGame.query.filter_by(campaign_id=campaign_id, game_id=game_id).first()
    if not campaign_game:
        return jsonify({'message': 'Campaign does not have access to this game.'})

    game = Game.query.get_or_404(game_id)
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.campaign_type == 'score' and 'user_id' not in session:
        return redirect(url_for('auth.login'))

    game_template = get_game_template(game.name, campaign_id)
    if game_template:
        return game_template
    else:
        return jsonify({'message': 'Game not found.'})

@bp.route('/game-test', methods=['GET'])
def game_test():
    return '''
        <script src="/static/js/widget.js" data-campaign-id="6" data-game-id="1"></script>
    '''