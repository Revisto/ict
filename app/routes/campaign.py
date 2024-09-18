# app/routes/campaign.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Campaign, Coupon, Game, CampaignGame, UserCampaignScore
from app.decorators import login_required
from app import db

bp = Blueprint('campaign', __name__)

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    campaigns = Campaign.query.filter_by(user_id=user_id).order_by(Campaign.created_at.desc()).all()
    games = Game.query.all()
    for campaign in campaigns:
        campaign.total_coupons = Coupon.query.filter_by(campaign_id=campaign.id).count()
        campaign.used_coupons = Coupon.query.filter_by(campaign_id=campaign.id, used=True).count()
        campaign.remaining_coupons = campaign.total_coupons - campaign.used_coupons
        campaign.public_coupons = Coupon.query.filter_by(campaign_id=campaign.id, type='public').all()
        campaign.onetime_coupons = Coupon.query.filter_by(campaign_id=campaign.id, type='onetime').all()
        campaign_campaign_games = CampaignGame.query.filter_by(campaign_id=campaign.id).all()
        for campaign_game in campaign_campaign_games:
            campaign_game.game = Game.query.get(campaign_game.game_id)
        campaign.games = campaign_campaign_games
        campaign.user_score = UserCampaignScore.query.filter_by(user_id=user_id, campaign_id=campaign.id).first()
    return render_template('dashboard.html', campaigns=campaigns, games=games)


@bp.route('/user_dashboard')
@login_required
def user_dashboard():
    user_id = session['user_id']
    campaigns = Campaign.query.all()
    for campaign in campaigns:
        campaign.user_score = UserCampaignScore.query.filter_by(user_id=user_id, campaign_id=campaign.id).first()
    return render_template('user_dashboard.html', campaigns=campaigns)

@bp.route('/create_campaign', methods=['POST'])
def create_campaign():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    name = request.form['name']
    user_id = session['user_id']
    campaign_type = request.form['campaign_type']
    new_campaign = Campaign(name=name, user_id=user_id, campaign_type=campaign_type)
    db.session.add(new_campaign)
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))

@bp.route('/upload_coupons/<int:campaign_id>', methods=['POST'])
def upload_coupons(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    codes = request.form['codes'].split(',')
    coupon_type = request.form['type']
    usage_limit = request.form.get('usage_limit', type=int)
    for code in codes:
        if coupon_type == "onetime":
            usage_limit = 1
        new_coupon = Coupon(campaign_id=campaign_id, code=code.strip(), type=coupon_type, usage_limit=usage_limit)
        db.session.add(new_coupon)
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))

@bp.route('/update_webservice_url/<int:campaign_id>', methods=['POST'])
def update_webservice_url(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    webservice_url = request.form['webservice_url']
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.webservice_url = webservice_url
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))

@bp.route('/delete_webservice_url/<int:campaign_id>', methods=['POST'])
def delete_webservice_url(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.webservice_url = None
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))

@bp.route('/select_games/<int:campaign_id>', methods=['POST'])
def select_games(campaign_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    game_ids = request.form.getlist('game_ids')
    for game_id in game_ids:
        if CampaignGame.query.filter_by(campaign_id=campaign_id, game_id=game_id).first():
            continue
        game = Game.query.get(game_id)
        embed_code = f'<script src="/static/js/widget.js" data-campaign-id="{campaign_id}" data-game-id="{game_id}"></script>'
        new_campaign_game = CampaignGame(campaign_id=campaign_id, game_id=game_id, embed_code=embed_code)
        db.session.add(new_campaign_game)
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))
