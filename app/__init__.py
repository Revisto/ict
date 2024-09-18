# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app.admin import register_admin_views
from app.services.game_sync_service import sync_games_with_db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import auth, campaign, widget, game, dashboard
    app.register_blueprint(auth.bp, name='auth')
    app.register_blueprint(campaign.bp, name='campaign')
    app.register_blueprint(widget.bp, name='widget')
    app.register_blueprint(game.bp, name='game')
    app.register_blueprint(dashboard.bp, name='dashboard')

    register_admin_views(app)

    with app.app_context():
        sync_games_with_db()

    return app