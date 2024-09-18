# app/services/game_sync_service.py
import json
import os
from app.models import Game
from app import db

def load_games_from_json():
    with open('app/config/games.json') as f:
        return json.load(f)['games']

def sync_games_with_db():
    games = load_games_from_json()
    for game_data in games:
        game = Game.query.get(game_data['id'])
        if game:
            game.name = game_data['name']
            game.description = game_data['description']
            game.score_increment = game_data['score_increment']
        else:
            game = Game(
                id=game_data['id'],
                name=game_data['name'],
                description=game_data['description'],
                score_increment=game_data['score_increment']
            )
            db.session.add(game)
    db.session.commit()