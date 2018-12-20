import datetime
import json
from flask import Flask, jsonify, request
from flask import Blueprint
from api.models import User, Incident
from flask_jwt_extended import (create_access_token,
                                JWTManager, jwt_required, 
                                get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

blueprint = Blueprint('application', __name__)
incidents = []
redflags = []
users = []


@blueprint.route('/')
def home():
    """A welcoming route to my api"""

    return jsonify({
        'message': 'Welcome to bekeplar\'s iReporter app.',
        'status': '200'
    }), 200


@blueprint.route('/signup', methods=['POST'])
def signup():
    """This function is used to create a new user."""
    data = request.get_json()
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
    error = user.validate_input(user)
    exists = user.check_user_exist(email, username)
    if error != None:
        return jsonify({'Error': error}), 400
    if not exists:
        password_hash = generate_password_hash(password, method='sha256')
        user.create_user(username, password_hash)
        users.append(user.__dict__)
        return jsonify({
            'status': 201,
            'message': f'{username} successfully registered.',
            'data': user.__dict__
            }), 201
    else:
        return jsonify({'message': exists}), 401


@blueprint.route('/redflags', methods=['POST'])
def create_redflag():
    """
    Function that adds a redflag incident to incidents.
   
    """
    data = request.get_json()
    id = len(incidents)+1
    createdBy = data.get("createdBy")
    type = data.get('type')
    title = data.get('title')
    location = data.get('location')
    comment = data.get('comment')
    status = data.get('status')
    createdOn = datetime.datetime.utcnow()

    redflag = Incident(id, createdBy, type,
                       title, location, comment,
                       status, createdOn
                       )
    error = Incident.validate_input(redflag)                   
    exists = redflag.check_incident_exist(title)

    if error != None:
        return jsonify({'Error': error}), 40
    if not exists:
        redflags.append(redflag.__dict__)
        return jsonify({
            'status': 201, 
            'message': 'creted redflag reccord!',
            'id': id,
            'data': redflag.__dict__
            }), 201
    else:
        return jsonify({'message': exists}), 401


