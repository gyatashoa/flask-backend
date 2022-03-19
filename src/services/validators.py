from datetime import datetime
import validators
from src.database import User


def register_validations(body: dict):
    email: str = body.get('email', None)
    password: str = body.get('password', None)
    dob: str = body.get('dob', '')
    if not validators.email(email):
        return 'Invalid email'

    if User.query.filter_by(email=email).first():
        return 'Email already taken'

    if body.get('first_name', None) is None:
        return 'First Name is required'

    if body.get('last_name', None) is None:
        return 'Last name is required'

    if body.get('dob', None) is None:
        return 'Date of birth is required'

    try:
        datetime.strptime(dob, '%d %m %Y')
    except ValueError as valueError:
        return 'Wrong date of birth format'

    if body.get('gender', None) is None:
        return 'Gender is required'

    if len(password) < 6:
        return "Password can't be lesser than 6 characters"


def login_validators(body: dict):
    email: str = body.get('email', None)
    password: str = body.get('password', None)
    if email is None:
        return 'Email is required'

    if not validators.email(email):
        return 'Invalid email'

    if password is None:
        return 'Password is required'

    if len(password) < 6:
        return "Password can't be lesser than 6 characters"
