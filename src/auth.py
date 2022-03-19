from flask import Blueprint, jsonify, request
from .services.validators import register_validations, login_validators
from .services.auth_services import save_user, check_login_credentials, get_user_details
from src.constants.http_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .constants import BASE_AUTH_URL
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


auth = Blueprint("auth", __name__, url_prefix=BASE_AUTH_URL)


@auth.post('register/')
@auth.post('register')
def register():
    msg = register_validations(request.json)
    if msg is not None:
        return jsonify({
            'error': {
                'message': msg,
            }
        }), HTTP_400_BAD_REQUEST
    res = save_user(request.json)
    if res is None:
        return jsonify({"message": "user created",
                        "user": {
                            "email": request.json['email']
                        }}), HTTP_201_CREATED
    return jsonify({"error": {
        "message": "Something went wrong on the server, please try again later"
    }}), HTTP_500_INTERNAL_SERVER_ERROR


@auth.post('login/')
@auth.post('login')
def login():
    msg = login_validators(request.json)
    if msg is not None:
        return jsonify({
            'error': {
                'message': msg
            }
        }), HTTP_400_BAD_REQUEST
    return check_login_credentials(request.json)


@auth.get('profile/')
@auth.get('profile')
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    return jsonify(get_user_details(user_id)), HTTP_200_OK


@auth.get('refresh/')
@auth.get('refresh')
@jwt_required(refresh=True)
def get_new_access_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(user_id)
    return jsonify({'access_token': access_token}), HTTP_200_OK
