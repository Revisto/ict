# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db
from app.load_default_games import load_default_games
from app.admin import register_admin_views

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import auth, campaign, widget, game, dashboard, analytics
    app.register_blueprint(auth.bp, name='auth')
    app.register_blueprint(campaign.bp, name='campaign')
    app.register_blueprint(widget.bp, name='widget')
    app.register_blueprint(game.bp, name='game')
    app.register_blueprint(dashboard.bp, name='dashboard')
    app.register_blueprint(analytics.bp, name='analytics')

    #register_admin_views(app)

    with app.app_context():
        db.create_all()
        load_default_games()

    return app