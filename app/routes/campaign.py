# app/routes/campaign.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.models import Campaign, Coupon, Game, CampaignGame, UserCampaignScore
from app.services.analytics_service import log_general_event
from app.decorators import company_required
from app import db

bp = Blueprint('campaign', __name__)

@bp.route('/create_campaign', methods=['POST'])
@company_required
def create_campaign():
    name = request.form['name']
    company_id = session['company_id']
    campaign_type = request.form['campaign_type']
    new_campaign = Campaign(name=name, company_id=company_id, campaign_type=campaign_type)
    db.session.add(new_campaign)
    db.session.commit()
    log_general_event(new_campaign.id, company_id, 'campaign_created', {'name': name, 'campaign_type': campaign_type})
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/upload_coupons/<int:campaign_id>', methods=['POST'])
@company_required
def upload_coupons(campaign_id):
    codes = request.form['codes'].split(',')
    coupon_type = request.form['type']
    usage_limit = request.form.get('usage_limit', type=int)
    for code in codes:
        if coupon_type == "onetime":
            usage_limit = 1
        new_coupon = Coupon(campaign_id=campaign_id, code=code.strip(), type=coupon_type, usage_limit=usage_limit)
        db.session.add(new_coupon)
    db.session.commit()
    log_general_event(campaign_id, session['company_id'], 'coupons_uploaded', {'count': len(codes), 'coupon_type': coupon_type})
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/update_webservice_url/<int:campaign_id>', methods=['POST'])
@company_required
def update_webservice_url(campaign_id):
    webservice_url = request.form['webservice_url']
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.webservice_url = webservice_url
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/delete_webservice_url/<int:campaign_id>', methods=['POST'])
@company_required
def delete_webservice_url(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.webservice_url = None
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/select_games/<int:campaign_id>', methods=['POST'])
@company_required
def select_games(campaign_id):
    game_ids = request.form.getlist('game_ids')
    for game_id in game_ids:
        campaign_game = CampaignGame.query.filter_by(campaign_id=campaign_id, game_id=game_id).first()
        if campaign_game:
            continue
        campaign = Campaign.query.get(campaign_id)
        game = Game.query.get(game_id)
        if game.type != campaign.campaign_type:
            return jsonify({'message': 'Unallowed game.'}), 400
        embed_code = f'<script src="http://127.0.0.1:5000/static/js/widget.js" data-campaign-id="{campaign_id}" data-game-id="{game_id}"></script>'
        new_campaign_game = CampaignGame(campaign_id=campaign_id, game_id=game_id, embed_code=embed_code)
        db.session.add(new_campaign_game)
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))

@bp.route('/campaigns', methods=['GET'])
def list_campaigns():
    campaigns = Campaign.query.filter_by(campaign_type='score').all()
    return render_template('campaigns.html', campaigns=campaigns)

@bp.route('/leaderboard/<int:campaign_id>', methods=['GET'])
def leaderboard(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    if campaign.campaign_type != 'score':
        return jsonify({'message': 'Invalid campaign type.'}), 400
    
    # Query the leaderboard for the selected campaign
    leaderboard = UserCampaignScore.query.filter_by(campaign_id=campaign_id).order_by(UserCampaignScore.score.desc()).all()
    return render_template('leaderboard.html', campaign=campaign, leaderboard=leaderboard)