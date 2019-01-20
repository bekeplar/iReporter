import datetime
import json
from database.db import DatabaseConnection
from flask import jsonify, request, Blueprint
from api.validators.user import Validation
from api.models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user blueprint', __name__)
db = DatabaseConnection()


@user_blueprint.route('/auth/signup', methods=['POST'])
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
    exists = user.check_user_exist()

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
    db.add_user(id, firstname, lastname,
                othernames, email, password_hash,
                username, registered, isAdmin)
    access_token = create_access_token(username)
    return jsonify({
        'status': 201,
        'token': access_token,
        'message': f'{username} successfully registered.',
        'user': user.__dict__
        }), 201


@user_blueprint.route('/auth/login', methods=['POST'])
def login():
    """This function allows a registered user to login"""
    data = json.loads(request.data)

    username = data.get('username')
    password = data.get('password')

    error = Validation.login_validate(username, password)

    if error != None:
        return jsonify({'Error': error}), 400

    db = DatabaseConnection()
    user = db.login(username)
    if user == None:
        return jsonify({'message': 'Wrong login credentials.'}), 400

    if check_password_hash(user['password'], password) and user['username'] == username:
        access_token = create_access_token(username)
        return jsonify({
            'status': 200,
            'token': access_token,
            'message': f'{username} successfully logged in.'
        }), 200
    else:
        return jsonify({'message': 'Wrong login credentials.'}), 400
     