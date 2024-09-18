# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.decorators import validate_uuid
from app.models import Company, User, GameAnalytics, UserCampaignScore
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_company = Company(username=username, password=password)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('auth.company_login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        company = Company.query.filter_by(username=username).first()
        if company and check_password_hash(company.password, password):
            session['company_id'] = company.id
            return redirect(url_for('dashboard.dashboard'))
    return render_template('login.html')

@bp.route('/authenticate', methods=['GET', 'POST'])
@validate_uuid
def authenticate(user):
    if request.method == 'POST':
        telephone = request.form['telephone']
        password = request.form['password']
        existing_user = User.query.filter_by(telephone=telephone).first()
        
        if existing_user:
            # Option 1: There is already this unique telephone
            if check_password_hash(existing_user.password, password):
                old_uuid = user.id
                
                # Sum up the old_uuid scores to existing_user
                old_scores = UserCampaignScore.query.filter_by(user_id=old_uuid).all()
                for old_score in old_scores:
                    existing_score = UserCampaignScore.query.filter_by(user_id=existing_user.id, campaign_id=old_score.campaign_id).first()
                    if existing_score:
                        existing_score.score += old_score.score
                    else:
                        old_score.user_id = existing_user.id
                        db.session.add(old_score)
                
                # Replace GameAnalytics old user_ids to existing_user
                GameAnalytics.query.filter_by(user_id=old_uuid).update({'user_id': existing_user.id})
                
                # Delete the old user object
                db.session.delete(User.query.get(old_uuid))
                db.session.commit()
                
                return jsonify({'uuid': existing_user.id})
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
        else:
            # Option 2: No Matched telephone
            user.telephone = telephone
            user.password = generate_password_hash(password)
            db.session.commit()
            return jsonify({'uuid': user.id})
    
    return render_template('authenticate.html')