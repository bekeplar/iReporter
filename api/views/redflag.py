import datetime
import json
from database.db import DatabaseConnection
from flask import jsonify, request, Blueprint
from api.validators.incident import Validators
from api.models.incident import Incident, incidents
from flask_jwt_extended import jwt_required, get_jwt_identity
db = DatabaseConnection()
blueprint = Blueprint('application', __name__)


@blueprint.route('/')
def home():
    """A welcoming route to my api"""
    return jsonify({
        'message': 'Welcome to bekeplar\'s iReporter app.',
        'status': '200'
    }), 200


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

