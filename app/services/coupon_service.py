# app/services/coupon_service.py
from app.models import Coupon, Campaign
from app import db
from app.services.analytics_service import log_general_event
import random
import requests

def handle_coupon_generation(campaign_id):
    result = generate_public_coupon(campaign_id)
    if result:
        return result

    result = generate_onetime_coupon(campaign_id)
    if result:
        return result

    campaign = Campaign.query.get(campaign_id)
    if campaign.webservice_url:
        result = generate_realtime_coupon(campaign)
        if result:
            return result

    return None

def generate_public_coupon(campaign_id):
    coupon = Coupon.query.filter_by(campaign_id=campaign_id, type='public', used=False).first()
    if coupon:
        if coupon.usage_limit is None or coupon.usage_count < coupon.usage_limit:
            coupon.usage_count += 1
            if coupon.usage_limit is not None and coupon.usage_count >= coupon.usage_limit:
                coupon.used = True
            db.session.commit()
            log_general_event(campaign_id, None, 'coupon_given', {'coupon_code': coupon.code})
            return {'coupon_code': coupon.code}
        else:
            return None
    return None

def generate_onetime_coupon(campaign_id):
    coupon = Coupon.query.filter_by(campaign_id=campaign_id, type='onetime', used=False).first()
    if coupon:
        coupon.used = True
        db.session.commit()
        log_general_event(campaign_id, None, 'coupon_given', {'coupon_code': coupon.code})
        return {'coupon_code': coupon.code}
    return None

def generate_realtime_coupon(campaign):
    coupon_code = generate_coupon_code()
    if validate_realtime_coupon(campaign.webservice_url, coupon_code):
        log_general_event(campaign.id, None, 'copuon_generated', {'coupon_code': coupon_code})
        return {'coupon_code': coupon_code}
    else:
        return None

def validate_realtime_coupon(webservice_url, coupon_code):
    params = {"coupon_code": coupon_code}
    response = requests.get(webservice_url, params=params)
    return True
    return response.status_code == 200 and response.json().get("valid", False)

def generate_coupon_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))