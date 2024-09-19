# app/models.py
import uuid
from datetime import datetime
from .extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    campaigns = db.relationship('Campaign', backref='company', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    telephone = db.Column(db.String(20), nullable=True, unique=True)
    password = db.Column(db.String(200), nullable=True)
    scores = db.relationship('UserCampaignScore', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    campaign_type = db.Column(db.String(20), nullable=False)  # 'score' or 'coupon'
    webservice_url = db.Column(db.String(200), nullable=True)
    scores = db.relationship('UserCampaignScore', backref='campaign', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCampaignScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(20), nullable=False)  # 'score' or 'coupon'
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)  # For private games
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
    game = db.relationship('Game', backref='campaign_games')

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # Add this line
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    embed_code = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GameAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # e.g., 'wrong_answer', 'correct_answer'
    event_data = db.Column(db.JSON, nullable=True)  # Additional data specific to the event
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'game_id': self.game_id,
            'user_id': self.user_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'created_at': self.created_at.isoformat()
        }

class GeneralAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # e.g., 'coupon_given', 'game_attempt'
    event_data = db.Column(db.JSON, nullable=True)  # Additional data specific to the event
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'company_id': self.company_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'created_at': self.created_at.isoformat()
        }