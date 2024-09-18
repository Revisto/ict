from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import User, Campaign, Coupon, CampaignGame, Widget, Game
from .extensions import db

def register_admin_views(app):
    admin = Admin(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Campaign, db.session))
    admin.add_view(ModelView(Coupon, db.session))
    admin.add_view(ModelView(CampaignGame, db.session))
    admin.add_view(ModelView(Widget, db.session))
    admin.add_view(ModelView(Game, db.session))