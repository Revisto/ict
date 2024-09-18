from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app.admin import register_admin_views

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import auth, campaign, widget
    app.register_blueprint(auth.bp, name='auth')
    app.register_blueprint(campaign.bp, name='campaign')
    app.register_blueprint(widget.bp, name='widget')

    #register_admin_views(app)

    return app
