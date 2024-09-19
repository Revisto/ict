# app/routes/dashboard.py
import os
from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models import Campaign, Coupon, Game, CampaignGame, UserCampaignScore
from app.decorators import company_required
from app import db

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard')
@company_required
def dashboard():
    company_id = session['company_id']
    campaigns = Campaign.query.filter_by(company_id=company_id).order_by(Campaign.created_at.desc()).all()
    games = Game.query.all()
    company_games = Game.query.filter_by(company_id=company_id).all()
    games = games + company_games
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
    return render_template('dashboard.html', campaigns=campaigns, games=games)