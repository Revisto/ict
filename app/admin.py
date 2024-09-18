# app/admin.py
from flask import redirect, url_for, request, session
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from .models import User, Campaign, Coupon, CampaignGame, Widget, Game
from .extensions import db

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(MyAdminIndexView, self).index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return True

class UserAdmin(SecureModelView):
    column_list = ('id', 'username', 'is_company', 'scores', 'created_at')
    form_columns = ('username', 'password', 'is_company', 'scores')

class CampaignAdmin(SecureModelView):
    column_list = ('id', 'name', 'user_id', 'campaign_type', 'created_at')
    form_columns = ('name', 'user_id', 'campaign_type')

class CouponAdmin(SecureModelView):
    column_list = ('id', 'code', 'campaign_id', 'used', 'usage_limit')
    form_columns = ('code', 'campaign_id', 'used', 'usage_limit')

class CampaignGameAdmin(SecureModelView):
    column_list = ('id', 'campaign_id', 'game_id')
    form_columns = ('campaign_id', 'game_id')

class WidgetAdmin(SecureModelView):
    column_list = ('id', 'campaign_id', 'embed_code')
    form_columns = ('name', 'campaign_id', 'embed_code')

class GameAdmin(SecureModelView):
    column_list = ('id', 'name', 'description')
    form_columns = ('name', 'description')

def register_admin_views(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(UserAdmin(User, db.session, name='UserAdmin', endpoint='admin_user'))
    admin.add_view(CampaignAdmin(Campaign, db.session, name='CampaignAdmin', endpoint='admin_campaign'))
    admin.add_view(CouponAdmin(Coupon, db.session, name='CouponAdmin', endpoint='admin_coupon'))
    admin.add_view(CampaignGameAdmin(CampaignGame, db.session, name='CampaignGameAdmin', endpoint='admin_campaign_game'))
    admin.add_view(WidgetAdmin(Widget, db.session, name='WidgetAdmin', endpoint='admin_widget'))
    admin.add_view(GameAdmin(Game, db.session, name='GameAdmin', endpoint='admin_game'))