from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from app.models import Campaign, Widget, Coupon
from app import db
import random
import requests

bp = Blueprint('widget', __name__)

@bp.route('/generate_widget/<int:campaign_id>')
def generate_widget(campaign_id):
    embed_code = f'<iframe src="/widget/{campaign_id}" width="300" height="400"></iframe>'
    new_widget = Widget(campaign_id=campaign_id, embed_code=embed_code)
    db.session.add(new_widget)
    db.session.commit()
    return jsonify({'embed_code': embed_code})

@bp.route('/widget/<int:campaign_id>')
def widget(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    coupons = Coupon.query.filter_by(campaign_id=campaign_id).all()
    return render_template('widget.html', campaign=campaign, coupons=coupons)

@bp.route('/game/<int:campaign_id>', methods=['GET', 'POST'])
def game(campaign_id):
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
        return render_template('game.html', num1=num1, num2=num2, campaign_id=campaign_id)

def handle_coupon_generation(campaign_id):
    # Try to generate a public coupon first
    result = generate_public_coupon(campaign_id)
    if result:
        return result

    # If no public coupon is available, try to generate a one-time coupon
    result = generate_onetime_coupon(campaign_id)
    if result:
        return result

    # If no one-time coupon is available, try to generate a real-time coupon
    campaign = Campaign.query.get(campaign_id)
    if campaign.webservice_url:
        return generate_realtime_coupon(campaign)

    return {'message': 'Sorry, no more coupons available.'}

def generate_public_coupon(campaign_id):
    coupon = Coupon.query.filter_by(campaign_id=campaign_id, type='public', used=False).first()
    if coupon:
        if coupon.usage_limit is None or coupon.usage_count < coupon.usage_limit:
            coupon.usage_count += 1
            if coupon.usage_limit is not None and coupon.usage_count >= coupon.usage_limit:
                coupon.used = True
            db.session.commit()
            return {'message': 'Correct! Here is your coupon code:', 'coupon': coupon.code}
        else:
            return {'message': 'Sorry, this coupon has reached its usage limit.'}
    return None

def generate_onetime_coupon(campaign_id):
    coupon = Coupon.query.filter_by(campaign_id=campaign_id, type='onetime', used=False).first()
    if coupon:
        coupon.used = True
        db.session.commit()
        return {'message': 'Correct! Here is your coupon code:', 'coupon': coupon.code}
    return None

def generate_realtime_coupon(campaign):
    coupon_code = generate_coupon_code()
    if validate_realtime_coupon(campaign.webservice_url, coupon_code):
        new_coupon = Coupon(campaign_id=campaign.id, code=coupon_code, type='realtime', used=True)
        db.session.add(new_coupon)
        db.session.commit()
        return {'message': 'Correct! Here is your coupon code:', 'coupon': coupon_code}
    else:
        return {'message': 'Sorry, this coupon is not valid.'}

def validate_realtime_coupon(webservice_url, coupon_code):
    params = {"coupon_code": coupon_code}
    response = requests.get(webservice_url, params=params)
    #return response.status_code == 200 and response.json().get("valid", False)
    return True

def generate_coupon_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))