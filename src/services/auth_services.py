from datetime import timedelta
import os
from flask import jsonify
from src.database import db
from datetime import datetime
from src.database import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_refresh_token, create_access_token
from src.constants.http_codes import HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST


def save_user(body: dict):
    try:
        hashed_password = generate_password_hash(body['password'])
        dob = datetime.strptime(body['dob'], '%d %m %Y')
        user = User(
            email=body['email'],
            password=hashed_password,
            first_name=body['first_name'],
            last_name=body['last_name'],
            other_name=body.get('other_name', None),
            gender=body['gender'],
            dob=dob
        )
        db.session.add(user)
        db.session.commit()
        # db.session.commit()
    except Exception as e:
        return e


def check_login_credentials(body: dict):
    email: str = body.get('email', '')
    password: str = body.get('password', '')
    user: User = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            access = create_access_token(
                user.id, expires_delta=timedelta(days=int(os.environ.get(
                    'JWT_ACCESS_TOKEN_EXPIRES'
                ))))
            refresh = create_refresh_token(
                user.id, expires_delta=timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))))
            return jsonify({
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'other_name': user.other_name,
                    'dob': user.dob,
                    'gender': user.gender
                },
                'tokens': {
                    'refresh': refresh,
                    'access': access
                }
            }), HTTP_202_ACCEPTED
    return jsonify({'error': {
        'message': 'Invalid credentials'
    }}), HTTP_400_BAD_REQUEST


def get_user_details(user_id: int):
    user: User = User.query.filter_by(id=user_id).first()
    return {'data': user.transform_user_to_dict()}
