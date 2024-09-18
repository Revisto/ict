# app/models.py
from datetime import datetime
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_company = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)  # Only for users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_type = db.Column(db.String(20), nullable=False)  # 'coupon' or 'score'
    webservice_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    used = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(20), nullable=False)  # 'public', 'realtime', 'onetime'
    usage_limit = db.Column(db.Integer, nullable=True)  # Only for public coupons
    usage_count = db.Column(db.Integer, default=0)  # Only for public coupons
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CampaignGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    embed_code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Add this line
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    embed_code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)