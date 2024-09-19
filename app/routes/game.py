# app/routes/game.py
import os
from flask import Blueprint, jsonify, request, redirect, url_for, session
from app.models import Campaign, Game, UserCampaignScore, Coupon, CampaignGame
from app.decorators import company_required
from app.services.game_service import render_game_template
from app.decorators import validate_uuid
from app import db

bp = Blueprint('game', __name__)

@bp.route('/popup/<int:campaign_id>/<int:game_id>', methods=['GET'])
@validate_uuid
def popup(user, campaign_id, game_id):
    campaign_game = CampaignGame.query.filter_by(campaign_id=campaign_id, game_id=game_id).first()
    if not campaign_game:
        return jsonify({'message': 'Campaign does not have access to this game.'})

    game = Game.query.get_or_404(game_id)
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.campaign_type == 'score' and not user.telephone:
        return redirect(url_for('auth.authenticate'))
    
    print("----------------")
    game_template = render_game_template(game, campaign_id)
    if game_template:
        return game_template
    else:
        return jsonify({'message': 'Game not found.'})

@bp.route('/game/get_coupon/<int:campaign_id>', methods=['GET'])
@validate_uuid
def get_coupon(user, campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.campaign_type != 'coupon':
        return jsonify({'message': 'Invalid campaign type.'}), 400

    coupon = Coupon.query.filter_by(campaign_id=campaign_id, used=False).first()
    if not coupon:
        return jsonify({'message': 'No available coupons.'}), 404

    coupon.used = True
    db.session.commit()
    return jsonify({'coupon_code': coupon.code})

@bp.route('/game/add_score/<int:campaign_id>', methods=['POST'])
@validate_uuid
def add_score(user, campaign_id):
    if not user.telephone:
        return jsonify({'message': 'Please authenticate to add a score.'}), 400
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.campaign_type != 'score':
        return jsonify({'message': 'Invalid campaign type.'}), 400

    print(request.json)
    score_increment = request.json.get('score_increment', 0)
    user_score = UserCampaignScore.query.filter_by(user_id=user.id, campaign_id=campaign_id).first()
    if not user_score:
        user_score = UserCampaignScore(user_id=user.id, campaign_id=campaign_id, score=0)
        db.session.add(user_score)

    print(score_increment)
    user_score.score += score_increment
    db.session.commit()
    return jsonify({'message': 'Score updated', 'score': user_score.score})

@bp.route('/game/get_user_score/<int:campaign_id>', methods=['GET'])
@validate_uuid
def get_user_score(user, campaign_id):
    if not user.telephone:
        return jsonify({'message': 'Please authenticate to get your score.'}), 400
    user_score = UserCampaignScore.query.filter_by(user_id=user.id, campaign_id=campaign_id).first()
    if not user_score:
        return jsonify({'score': 0})

    return jsonify({'score': user_score.score})

@bp.route('/upload_custom_game/<int:campaign_id>', methods=['POST'])
@company_required
def upload_custom_game(campaign_id):
    company_id = session['company_id']
    game_name = request.form.get('game_name')
    game_type = request.form.get('game_type')  # score or coupon
    game_file = request.files.get('game_file')

    if not game_name:
        return jsonify({'message': 'Game name is required'}), 400

    if game_type not in ['score', 'coupon']:
        return jsonify({'message': 'Invalid game type. Must be "score" or "coupon"'}), 400

    if not game_file:
        return jsonify({'message': 'Game file is required'}), 400

    game_name = f"{game_name} (Private)"
    filename = f"{company_id}_{game_name}.html"
    filepath = os.path.join('app', 'templates', 'custom_games', filename)
    game_file.save(filepath)

    new_game = Game(name=game_name, description='Custom Game', type=game_type, company_id=company_id)
    db.session.add(new_game)
    db.session.commit()

    return redirect(url_for('dashboard.dashboard'))

@bp.route('/game-test', methods=['GET'])
def game_test():
    return '''
        <script src="/static/js/widget.js" data-campaign-id="1" data-game-id="1"></script>
    '''