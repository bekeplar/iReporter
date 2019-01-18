import datetime
import json
from flask import jsonify, request, Blueprint
from api.validators.user import Validation
from api.models.user import User
from api.Helpers import create_user, login_user
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

users = list()
user_blueprint = Blueprint('user blueprint', __name__)


@user_blueprint.route('/signup', methods=['POST'])
def signup():
    """This function is used to create a new user."""
    data = json.loads(request.data)
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    othernames = data.get('othernames')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    username = data.get('username')
    registered = datetime.datetime.utcnow()
    isAdmin = data.get('isAdmin')
    password = data.get('password')

    user = User(firstname, lastname, othernames,
                email, phoneNumber, username,
                registered, isAdmin, password
                )
    error = Validation.validate_input(user)
    errors = Validation.validate_inputs(user)
    exists = [user for user in users if user['username'] == username or
              user['email'] == email]

    if error != None:
        return jsonify({'Error': error}), 400
    if errors != None:
        return jsonify({'Error': errors}), 400
    if exists:
        return jsonify({
            'message':  'user already registered.',
            'status': 406
            }), 406
    password_hash = generate_password_hash(password, method='sha256')
    create_user(username, password_hash)
    users.append(user.__dict__)
    return jsonify({
        'status': 201,
        'message': f'{username} successfully registered.',
        'data': user.__dict__
        }), 201


@user_blueprint.route('/login', methods=['POST'])
def login():
    """This function allows a registered user to login"""
    data = json.loads(request.data)

    username = data.get('username')
    password = data.get('password')

    error = Validation.login_validate(username, password)

    if error:
        return jsonify({'Error': error}), 400
    user = login_user(username, password)
    for user in users:
        if not user:
            return jsonify({
                'message': 'Wrong login credentials!',
                'status': 401
                }), 401
        check_password_hash(user['password'], password) and user['username'] == username,
        access_token = create_access_token(username)
        return jsonify({
            'token': access_token,
            'status': 200,
            'message': f'{username} successfully logged in.'
        }), 200
    else:
        return jsonify({
                'message': 'Wrong login credentials!',
                'status': 401
                }), 401
