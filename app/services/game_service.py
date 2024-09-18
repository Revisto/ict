# app/services/game_service.py
from flask import render_template, request, jsonify
import random
from app.models import CampaignGame, Game
from app.services.coupon_service import handle_coupon_generation

def sum_game(campaign_id):
    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        answer = int(request.form['answer'])
        if answer == num1 + num2:
            result = handle_coupon_generation(campaign_id)
            return jsonify(result)
        else:
            return jsonify({'message': 'Incorrect answer. Please try again.'})
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        return render_template('games/sum_game.html', num1=num1, num2=num2, campaign_id=campaign_id)

def multiply_game(campaign_id):
    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        answer = int(request.form['answer'])
        if answer == num1 * num2:
            result = handle_coupon_generation(campaign_id)
            return jsonify(result)
        else:
            return jsonify({'message': 'Incorrect answer. Please try again.'})
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        return render_template('games/multiply_game.html', num1=num1, num2=num2, campaign_id=campaign_id)

def get_game_template(game_name, campaign_id):
    if game_name == 'Sum Game':
        return sum_game(campaign_id)
    elif game_name == 'Multiply Game':
        return multiply_game(campaign_id)
    else:
        return None