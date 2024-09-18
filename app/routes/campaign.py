from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import Campaign, Coupon, Game, CampaignGame
from app import db

bp = Blueprint('campaign', __name__)

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    campaigns = Campaign.query.filter_by(user_id=user_id).all()
    games = Game.query.all()
    for campaign in campaigns:
        campaign.total_coupons = Coupon.query.filter_by(campaign_id=campaign.id).count()
        campaign.used_coupons = Coupon.query.filter_by(campaign_id=campaign.id, used=True).count()
        campaign.remaining_coupons = campaign.total_coupons - campaign.used_coupons
        campaign.public_coupons = Coupon.query.filter_by(campaign_id=campaign.id, type='public').all()
        campaign.onetime_coupons = Coupon.query.filter_by(campaign_id=campaign.id, type='onetime').all()
        campaign_campaign_games = CampaignGame.query.filter_by(campaign_id=campaign.id).all()
        for campaign_game in campaign_campaign_games:
            campaign_game.game = Game.query.get(campaign_game.game_id)  # Fetching the game details
        campaign.games = campaign_campaign_games
    return render_template('dashboard.html', campaigns=campaigns, games=games)

@bp.route('/create_campaign', methods=['POST'])
def create_campaign():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    name = request.form['name']
    user_id = session['user_id']
    new_campaign = Campaign(name=name, user_id=user_id)
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
        embed_code = f'<iframe src="/widget/{campaign_id}/{game_id}" width="300" height="400"></iframe>'
        new_campaign_game = CampaignGame(campaign_id=campaign_id, game_id=game_id, embed_code=embed_code)
        db.session.add(new_campaign_game)
    db.session.commit()
    return redirect(url_for('campaign.dashboard'))