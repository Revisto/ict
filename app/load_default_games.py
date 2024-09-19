# app/load_default_games.py
import json
from app import db
from app.models import Game
from flask import current_app

def load_default_games():
    with current_app.open_resource('config/default_games.json') as f:
        games_data = json.load(f)

    for game_data in games_data['games']:
        game = Game.query.filter_by(id=game_data['id']).first()
        if game:
            game.name = game_data['name']
            game.description = game_data['description']
            game.type = game_data['type']
        else:
            game = Game(
                id=game_data['id'],
                name=game_data['name'],
                description=game_data['description'],
                type=game_data['type']
            )
            db.session.add(game)
    db.session.commit()
