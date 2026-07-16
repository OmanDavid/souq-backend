from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
import secrets

auth_bp = Blueprint('auth', __name__)
reset_tokens = {}  # simple in-memory store; fine for capstone scope

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'user': {'id': user.id, 'name': user.name}}), 200

@auth_bp.route('/auth/reset-request', methods=['POST'])
def reset_request():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        token = secrets.token_urlsafe(16)
        reset_tokens[token] = user.id
        # in production: email this token/link to the user
        print(f"Reset token for {user.email}: {token}")
    return jsonify({'message': 'If that email exists, a reset link was sent'}), 200

@auth_bp.route('/auth/reset-confirm', methods=['POST'])
def reset_confirm():
    data = request.get_json()
    user_id = reset_tokens.get(data['token'])
    if not user_id:
        return jsonify({'error': 'Invalid or expired token'}), 400
    user = User.query.get(user_id)
    user.password_hash = generate_password_hash(data['new_password'])
    db.session.commit()
    del reset_tokens[data['token']]
    return jsonify({'message': 'Password updated'}), 200