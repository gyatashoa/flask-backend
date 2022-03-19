from flask import Blueprint, jsonify, request
from src.constants import BASE_PREDICTION_URL
from src.database import Prediction, db
from src.services.predict import get_symptoms as gt, make_prediction
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants.http_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

predictions = Blueprint("predictions", __name__,
                        url_prefix=BASE_PREDICTION_URL)


@predictions.get('predict')
@jwt_required()
def predict():
    user_id = get_jwt_identity()
    body: dict = request.json
    symptoms: list[str] = body.get('symptoms', [])
    if len(symptoms) == 0:
        return jsonify({'error': {'message': 'Invalid symptoms format'}}), HTTP_400_BAD_REQUEST
    predicted_value = make_prediction(symptoms)
    prediction = Prediction(user_id=user_id, disease_name=predicted_value)
    db.session.add(prediction)
    db.session.commit()
    return jsonify({'disease': predicted_value}), HTTP_201_CREATED


@predictions.get('symptoms')
def get_symptoms():
    data = {'symptoms': gt()}
    return jsonify(data), HTTP_200_OK
