# app/decorators.py
from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from app.models import User, Company
from app import db

def validate_uuid(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is required'}), 400
        uuid = auth_header.split(' ')[1] if ' ' in auth_header else None
        print("uuid: ", uuid)
        if not uuid:
            return jsonify({'message': 'UUID is required'}), 400
        user = User.query.get(uuid)
        if not user:
            user = User(id=uuid)
            db.session.add(user)
            db.session.commit()
        return f(user, *args, **kwargs)
    return decorated_function

def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'company_id' not in session:
            return redirect(url_for('auth.company_login'))
        company = Company.query.get(session.get('company_id'))
        if not company:
            return redirect(url_for('auth.company_login'))
        return f(*args, **kwargs)
    return decorated_function