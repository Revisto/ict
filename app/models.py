from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    webservice_url = db.Column(db.String(255), nullable=True)  # URL for real-time coupon generation

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    used = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(20), nullable=False)  # 'public', 'realtime', 'onetime'
    usage_limit = db.Column(db.Integer, nullable=True)  # Only for public coupons
    usage_count = db.Column(db.Integer, default=0)  # Only for public coupons

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    embed_code = db.Column(db.Text, nullable=False)