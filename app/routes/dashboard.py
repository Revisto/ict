# app/routes/dashboard.py
from flask import Blueprint, render_template, redirect, url_for, session
from app.models import Campaign, Coupon, Game, CampaignGame, UserCampaignScore
from app.decorators import login_required
from app import db

bp = Blueprint('dashboard', __name__)

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
