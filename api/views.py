import datetime
import json
from database.db import DatabaseConnection
from flask import jsonify, request, Blueprint
from api.validator import Validation, Validators
from api.models import User, Incident, incidents
from flask_jwt_extended import (create_access_token,
                                jwt_required, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash

blueprint = Blueprint('application', __name__)
db = DatabaseConnection()


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
    db.insert_user(id, firstname, lastname,
                   othernames, email, password_hash,
                   username, registered, isAdmin)
    return jsonify({
        'status': 201,
        'message': f'{username} successfully registered.',
        'data': user.__dict__
        }), 201


@blueprint.route('/login', methods=['POST'])
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
     

@blueprint.route('/redflags', methods=['POST'])
@jwt_required
def create_redflag():
    """
    Function that adds a redflag incident to list of redflags.
   
    """
    data = json.loads(request.data)
    id = len(incidents)+1
    createdBy = data.get('createdBy')
    type = data.get('type')
    title = data.get('title')
    location = data.get('location')
    comment = data.get('comment')
    status = 'draft'
    createdOn = datetime.datetime.utcnow()
    images = data.get('images')
    videos = data.get('videos')

    redflag = Incident(id, createdBy, type,
                       title, location, comment,
                       status, createdOn, images, videos
                       )
    error = Validators.validate_inputs(redflag)      
    exists = redflag.check_incident_exist()
    if error != None:
        return jsonify({'Error': error, 'status': 400}), 400
    if exists:
        return jsonify({
            'Error': 'Redflag record already reported!',
            'status': 406}), 406
    db.insert_redflag(id, createdBy, type,
                      title, location, comment,
                      status, createdOn, images, videos)
    return jsonify({
        'status': 201, 
        'message': 'created redflag reccord!',
        'id': id,
        'data': redflag.__dict__
        }), 201


@blueprint.route('/redflags', methods=['GET'])
@jwt_required
def get_all_redflags():
    """
    function to enable a user get all reported redflags
    :returns:
    The entire redflags reported by a user.
    """
    all_redflags = db.fetch_all_redflags()
    if not all_redflags:
        return jsonify({
            'satus': 400,
            'message': 'You haven/t reported any redflag!',
            'data': all_redflags
        }), 400
    return jsonify({
        'status': 200,
        'data': all_redflags,
        'message': 'These are your reports!'
    }), 200


@blueprint.route('/redflags/<int:id>', methods=['GET'])
@jwt_required
def get_specific_redflag(id):
    """
    This function enables a registered
    user fetch a specific redflag record.
    :params:
    :returns:
    For any given right id
    """
    try:
        get_one = db.fetch_redflag(id)
        if not get_one:
            return jsonify({'message': 'No such redflag record found!'}), 404
        return jsonify({
            'status': 404,
            'data': get_one,
            'message': 'Redflag record found succesfully.',
        }), 200
    except TypeError:
        return jsonify({'message': 'Redflag Id must be a number.'}), 400


@blueprint.route('/redflags/<int:id>', methods=['DELETE'])
@jwt_required
def delete_specific_redflag(id):
    """
    Function for deleting a specific redflag from the report.
    """
    try:
        username = get_jwt_identity()
        get_one = db.fetch_redflag(id)

        if username and get_one:
            db.delete_redflag(id)
            return jsonify({'message': 'Redflag record deleted succesfully.',
                            'data': get_one,
                            'status': 200
                            }), 200
        else:
            return jsonify({
                           'message': 'No such redflag record found!',
                           'status': 404
                           }), 404
    except TypeError:
        return jsonify({'message': 'Only the reporter can delete this.',
                        'status': 401}), 401

@blueprint.route('/redflags/<int:id>/status', methods=['PATCH'])
@jwt_required
def edit_status_of_redflag(id):
    """
    Function for editing the redflag status.
    """
    data = request.get_json()['status']
    try:
        get_one = db.fetch_redflag(id)
        if get_one:
            db.update_status(id, data)
            return jsonify({'status': 200,
                            'data': db.fetch_redflag(id),
                            'message': 'Redflag status successfully updated!'
                            }), 200
        else:
            return jsonify({'status': 404,
                            'message': 'No such redflag record found!'
                            }), 404
    except ValueError:
        return jsonify({
            'message': 'Please provide right inputs'
        }), 400


@blueprint.route('/redflags/<int:id>/location', methods=['PATCH'])
@jwt_required
def edit_location_of_redflag(id):
    """
    Function for editing the redflag location.
    """
    data = json.loads(request.data)
    location = data.get('location')
    try:
        get_one = db.fetch_redflag(id)
        if get_one:
            db.update_location(id, location)
            return jsonify({'status': 200,
                            'data': db.fetch_redflag(id),
                            'message': 'Redflag location successfully updated!'
                            }), 200
        else:
            return jsonify({'status': 404,
                            'message': 'No such redflag record found!'
                            }), 404
    except ValueError:
        return jsonify({
            'message': 'Please provide right inputs'
        }), 400


@blueprint.route('/redflags/<int:id>/comment', methods=['PATCH'])
@jwt_required
def edit_comment_of_redflag(id):
    """
    Function for editing the comment of a redflag.
    """
    data = json.loads(request.data)
    comment = data.get('comment')
    try:
        get_one = db.fetch_redflag(id)
        if get_one:
            db.update_comment(id, comment)
            return jsonify({'status': 200,
                            'data': db.fetch_redflag(id),
                            'message': 'Redflag comment successfully updated!'
                            }), 200
        else:
            return jsonify({'status': 404,
                            'message': 'No such redflag record found!'
                            }), 404
    except ValueError:
        return jsonify({
            'message': 'Please provide right inputs'
        }), 400


