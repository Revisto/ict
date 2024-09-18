# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        is_company = 'is_company' in request.form
        new_user = User(username=username, password=password, is_company=is_company)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            print(user)
            session['user_id'] = user.id
            session['is_company'] = user.is_company
            if user.is_company:
                return redirect(url_for('campaign.dashboard'))
            else:
                return redirect(url_for('campaign.user_dashboard'))
    return render_template('login.html')