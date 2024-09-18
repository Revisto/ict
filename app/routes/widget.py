# app/routes/widget.py
from flask import Blueprint, jsonify, request
from app.models import Widget
from app import db

bp = Blueprint('widget', __name__)

@bp.route('/generate_widget/<int:campaign_id>/<int:game_id>')
def generate_widget(campaign_id, game_id):
    embed_code = f'<script src="/static/js/widget.js" data-campaign-id="{campaign_id}" data-game-id="{game_id}"></script>'
    new_widget = Widget(campaign_id=campaign_id, embed_code=embed_code)
    db.session.add(new_widget)
    db.session.commit()
    return jsonify({'embed_code': embed_code})