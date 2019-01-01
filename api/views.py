import datetime
import json
from flask import jsonify, request
from flask import Blueprint
from api.validator import Validation, Validators
from api.models import User, Incident
from api.Helpers import (check_is_admin, get_user, check_user_exist,
                         create_user, check_incident_exist, login_user)
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash


blueprint = Blueprint('application', __name__)
incidents = []
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
    error = Validation.validate_input(user)
    errors = Validation.validate_inputs(user)
    exists = check_user_exist(email, username)
    if error != None:
        return jsonify({'Error': error}), 400
    if errors != None:
        return jsonify({'Error': errors}), 400
    
    if not exists:
        password_hash = generate_password_hash(password, method='sha256')
        create_user(username, password_hash)
        users.append(user.__dict__)
        return jsonify({
            'status': 201,
            'message': f'{username} successfully registered.',
            'data': user.__dict__
            }), 201
    else:
        return jsonify({'message': exists}), 401


@blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    error = Validation.login_validate(username, password)

    if error:
        return jsonify({'Error': error}), 400
    user = login_user(username)
    for user in users:

        if not user:
            return jsonify({
                'message': 'Wrong login credentials!',
                'status': 403
                }), 403
        check_password_hash(user['password'], password) and user['username'] == username
        access_token = create_access_token(username)
        return jsonify({
            'token': access_token,
            'status': 200,
            'message': f'{username} successfully logged in.'
        }), 200
    else:
        return jsonify({
            'message': 'Wrong login credentials!',
            'status': 403
        }), 403


@blueprint.route('/redflags', methods=['POST'])
@jwt_required
def create_redflag():
    """
    Function that adds a redflag incident to list of redflags.
   
    """
    data = request.get_json()
    id = len(incidents)+1
    createdBy = data.get("createdBy")
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
    exists = check_incident_exist(title)
    if error != None:
        return jsonify({'Error': error, 'status': 400}), 400
    if exists:
        return jsonify({'message': exists, 'status': 401}), 401
    incidents.append(redflag.__dict__)
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
    if len(incidents) == 0:
        return jsonify({
            'satus': 400,
            'message': 'You haven/t reported any redflag!'
        }), 400
    return jsonify({
        'status': 200,
        'data': [redflag for redflag in incidents],
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
    redflagId = int(id)
    for redflag in incidents:
        if int(redflag['id']) == redflagId:
            return jsonify({
                'status': 200,
                'data': redflag,
                'message': 'Redflag record found!'
                }), 200
    return jsonify({
        'status': 404,
        'message': 'No such redflag record found!'
        }), 404


@blueprint.route('/redflags/<int:id>', methods=['DELETE'])
def delete_specific_redflag(id):
    """
    Function for deleting a specific redflag from the report.
    """
    redflagId = int(id)
    for redflag in incidents:
        if int(redflag['id']) == redflagId:
            incidents.remove(redflag)
            return jsonify({
                'data': redflag,
                'status': 200,
                'id': id,
                'message': 'Redflag record  deleted!'
            }), 200
    return jsonify({'status': 404,
                   'message': 'No such redflag record found!'
          }), 404


@blueprint.route('/redflags/<int:id>/location', methods=['PATCH'])
def edit_location_of_redflag(id):
    data = json.loads(request.data)
    location = data['location']
    redflagId = int(id)
    for redflag in incidents:
        if int(redflag['id']) == redflagId:
            if redflag['status'] != 'draft':
                return jsonify({
                    'status': 400,
                    'message': 'Only draft status can be updated!'}), 400
            redflag['location'] = location
            return jsonify({
                'status': 200, 
                'data': redflag,
                'message': 'Redflag location successfully updated!'
                            }), 200
    return jsonify({'status': 404,
                    'message': 'No such redflag record found!'
                    }), 404


@blueprint.route('/redflags/<int:id>/comment', methods=['PATCH'])
def edit_comment_of_redflag(id):
    data = json.loads(request.data)
    comment = data['comment']
    redflagId = int(id)  
    for redflag in incidents:
        if int(redflag['id']) == redflagId:
            if redflag['status'] != 'draft':
                return jsonify({
                    'status': 400,
                    'message': 'Only draft status can be updated!'}), 400
            redflag['comment'] = comment
            return jsonify({'status': 200, 
                            'data': redflag,
                            'message': 'Redflag comment successfully updated!'
                            }), 200
    return jsonify({'status': 404,
                    'message': 'No such redflag record found!'
                    }), 404
