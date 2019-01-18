import datetime
import json
from flask import jsonify, request, Blueprint
from api.validators.incident import Validators
from api.models.incident import Incident
from api.Helpers import verify_status, check_status
from flask_jwt_extended import jwt_required
incidents = []
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
    _id = len(incidents)+1
    createdBy = data.get('createdBy')
    _type = data.get('type')
    title = data.get('title')
    location = data.get('location')
    comment = data.get('comment')
    status = 'draft'
    createdOn = datetime.datetime.utcnow()
    images = data.get('images')
    videos = data.get('videos')

    redflag = Incident(_id, createdBy, _type,
                       title, location, comment,
                       status, createdOn, images, videos
                       )
    error = Validators.validate_inputs(redflag)
    error1 = Validators.validate_media(redflag)     
    exists = [redflag for redflag in incidents if redflag['title'] == title]
    if error != None:
        return jsonify({'Error': error, 'status': 400}), 400
    if error1 != None:
        return jsonify({'Error': error, 'status': 400}), 400
    if exists:
        return jsonify({
            'Error': 'Redflag record already reported!',
            'status': 406}), 406
    incidents.append(redflag.__dict__)
    return jsonify({
        'status': 201, 
        'message': 'created redflag reccord!',
        'id': _id,
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
            'message': 'You haven/t reported any redflag!',
            'data': [redflag for redflag in incidents]
        }), 400
    return jsonify({
        'status': 200,
        'data': [redflag for redflag in incidents],
        'message': 'These are your reports!'
    }), 200


@blueprint.route('/redflags/<int:redflag_id>', methods=['GET'])
@jwt_required
def get_specific_redflag(redflag_id):
    """
    This function enables a registered
    user fetch a specific redflag record.
    :params:
    :returns:
    For any given right id
    """
    if len(incidents) == 0:
        return jsonify({
            'satus': 400,
            'data': [redflag for redflag in incidents],
            'message': 'You haven/t reported any redflag!'
        }), 400
    redflagId = int(redflag_id)
    for redflag in incidents:
        if int(redflag['_id']) == redflagId:
            return jsonify({
                'status': 200,
                'data': redflag,
                'message': 'Redflag record found!'
                }), 200
    return jsonify({
        'status': 404,
        'message': 'No such redflag record found!'
        }), 404


@blueprint.route('/redflags/<int:redflag_id>', methods=['DELETE'])
@jwt_required
def delete_specific_redflag(redflag_id):
    """
    Function for deleting a specific redflag from the report.
    """
    redflagId = int(redflag_id)
    for redflag in incidents:
        if int(redflag['_id']) == redflagId:
            incidents.remove(redflag)
            return jsonify({
                'data': redflag,
                'status': 200,
                'id': redflag_id,
                'message': 'Redflag record  deleted!'
            }), 200
    return jsonify({
        'status': 404,
        'message': 'No such redflag record found!'
            }), 404


@blueprint.route('/redflags/<int:redflag_id>/location', methods=['PATCH'])
@jwt_required
def edit_location_of_redflag(redflag_id):
    data = json.loads(request.data)
    location = data.get('location')
    redflagId = int(redflag_id)
    for redflag in incidents:
        if int(redflag['_id']) == redflagId:
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


@blueprint.route('/redflags/<int:redflag_id>/status', methods=['PATCH'])
@jwt_required
def edit_status_of_redflag(redflag_id):
    data = json.loads(request.data)
    status = data.get('status')
    RedflagId = int(redflag_id)
    error = verify_status(status)

    if error:
        return jsonify({'status': 400,
                        'error': 'error'
                        }), 400
    for redflag in incidents:
        if redflag['_id'] == RedflagId:
            redflag['status'] = status
            return jsonify({'status': 200, 
                            'data': redflag,
                            'message': 'Redflag status successfully updated!'
                            }), 200
    return jsonify({'status': 404,
                    'message': 'No such redflag record found!'
                    }), 404


@blueprint.route('/redflags/<int:redflag_id>/comment', methods=['PATCH'])
@jwt_required
def change_comment_of_redflag(redflag_id):
    data = json.loads(request.data)
    comment = data.get('comment')
    error = check_status()
    if error:
        return jsonify({
            'status': 400,
            'message': 'Only draft status can be updated!'}), 400
    RedflagId = int(redflag_id)
    for redflag in incidents:
        if redflag['_id'] == RedflagId:
            redflag['comment'] = comment
            return jsonify({'status': 200, 
                            'data': redflag,
                            'message': 'Redflag comment successfully updated!'
                            }), 200
    return jsonify({'status': 404,
                    'message': 'No such redflag record found!'
                    }), 404
