# app/services/game_service.py
from flask import render_template, request, jsonify, session
from app.services.reward_service import handle_game_reward
from app.services.analytics_service import log_game_event
import random
from app.models import Campaign, UserCampaignScore, Game

def sum_game(campaign_id):
    if request.method == 'POST':
        game = Game.query.filter_by(name='Sum Game').first()
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        answer = int(request.form['answer'])
        if answer == num1 + num2:
            result = handle_game_reward(campaign_id, game, session.get('user_id'))
            log_game_event(campaign_id, game.id, session.get('user_id'), 'correct_answer', {'num1': num1, 'num2': num2, 'answer': answer})
            return jsonify(result)
        else:
            log_game_event(campaign_id, game.id, session.get('user_id'), 'wrong_answer', {'num1': num1, 'num2': num2, 'answer': answer})
            return jsonify({'message': 'Incorrect answer. Please try again.'})
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        campaign = Campaign.query.get(campaign_id)
        user_score = UserCampaignScore.query.filter_by(user_id=session.get('user_id'), campaign_id=campaign_id).first()
        return render_template('games/sum_game.html', num1=num1, num2=num2, campaign=campaign, user_score=user_score)

def multiply_game(campaign_id):
    if request.method == 'POST':
        game = Game.query.filter_by(name='Multiply Game').first()
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        answer = int(request.form['answer'])
        if answer == num1 * num2:
            result = handle_game_reward(campaign_id, game, session.get('user_id'))
            log_game_event(campaign_id, game.id, session.get('user_id'), 'correct_answer', {'num1': num1, 'num2': num2, 'answer': answer})
            return jsonify(result)
        else:
            log_game_event(campaign_id, game.id, session.get('user_id'), 'wrong_answer', {'num1': num1, 'num2': num2, 'answer': answer})
            return jsonify({'message': 'Incorrect answer. Please try again.'})
    else:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        campaign = Campaign.query.get(campaign_id)
        user_score = UserCampaignScore.query.filter_by(user_id=session.get('user_id'), campaign_id=campaign_id).first()
        return render_template('games/multiply_game.html', num1=num1, num2=num2, campaign=campaign, user_score=user_score)

def get_game_template(game_name, campaign_id):
    if game_name == 'Sum Game':
        return sum_game(campaign_id)
    elif game_name == 'Multiply Game':
        return multiply_game(campaign_id)
    else:
        return None