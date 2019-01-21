import json
from database.db import DatabaseConnection
from flask import jsonify, request, Blueprint
from api.controllers.redflag import RedflagController
from flask_jwt_extended import jwt_required
db = DatabaseConnection()
blueprint = Blueprint('application', __name__)

redflag_controller = RedflagController()


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
    return redflag_controller.create_new_redflag(data)


@blueprint.route('/redflags', methods=['GET'])
@jwt_required
def get_all_redflags():
    """
    View function containing route for getting all redflags.
    """

    return redflag_controller.fetch_all_redflags()


@blueprint.route('/redflags/<int:id>', methods=['GET'])
@jwt_required
def get_specific_redflag(id):
    """
    View function for getting a specific redflag from the report.
    """
    return redflag_controller.fetch_one_redflag()
    

@blueprint.route('/redflags/<int:id>', methods=['DELETE'])
@jwt_required
def delete_specific_redflag(id):
    """
    View function with route for getting a specific redflag from the report.
    """
    return redflag_controller.delete_one_redflag()


@blueprint.route('/redflags/<int:id>/status', methods=['PATCH'])
@jwt_required
def edit_status_of_redflag(redflag_id):
    """
    Function for editing the redflag status.
    """
    data = request.get_json()['status']
    return redflag_controller.update_status(data)


@blueprint.route('/redflags/<int:redflag_id>/location', methods=['PATCH'])
@jwt_required
def edit_location_of_redflag(redflag_id):
    """
    Function wirh a route for editing the redflag location.
    """
    data = json.loads(request.data)
    return redflag_controller.update_location(data)


@blueprint.route('/redflags/<int:redflag_id>/comment', methods=['PATCH'])
@jwt_required
def edit_comment_of_redflag(redflag_id):
    """
    Function with route for editing the comment of a redflag.
    """
    data = json.loads(request.data)
    return redflag_controller.update_comment(data)

