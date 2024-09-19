# app/services/game_service.py
from flask import render_template
from app.models import Campaign

def render_game_template(game, campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if game.company_id is None: # Public game
        return render_template(f'games/{game.name}.html', campaign=campaign)
    else:
        return render_template(f'custom_games/{game.company_id}_{game.name}.html', campaign=campaign)