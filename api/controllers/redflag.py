import datetime
import uuid
from database.db import DatabaseConnection
from flask import jsonify
from api.validators.incident import Validators
from flask_jwt_extended import get_jwt_identity
from api.models.incident import Incident
db = DatabaseConnection()


class RedflagController:
    """
    Class containing all logic connecting redflag views and models.
    """

    def create_new_redflag(self, data):
        """
        Method for creating a new redflag.
        """
        incident_id = uuid.uuid4()
        createdBy = data.get('createdBy')
        type = data.get('type')
        title = data.get('title')
        location = data.get('location')
        comment = data.get('comment')
        status = 'draft'
        createdOn = datetime.datetime.utcnow()
        images = data.get('images')
        videos = data.get('videos')

        redflag = Incident(incident_id, createdBy, type,
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
        db.insert_redflag(incident_id, createdBy, type,
                          title, location, comment,
                          status, createdOn, images, videos)
        return jsonify({
            'status': 201, 
            'message': 'created redflag reccord!',
            'id': incident_id,
            'data': redflag.__dict__
            }), 201

    def fetch_all_redflags(self):
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

    def fetch_one_redflag(self, redflag_id):
        """
        This method enables a registered
        user fetch a specific redflag record.
        :params:
        :returns:
        For any given right id
        """
        try:
            get_one = db.fetch_redflag(redflag_id)
            if not get_one:
                return jsonify({
                    'status': 404,
                    'message': 'No such redflag record found!'}), 404
            return jsonify({
                'status': 404,
                'data': get_one,
                'message': 'Redflag record found succesfully.',
            }), 200
        except TypeError:
            return jsonify({'message': 'Redflag Id must be a number.'}), 400

    def delete_one_redflag(self, redflag_id):
        """
        A method for deleting a specific redflag from the report.
        """
        try:
            username = get_jwt_identity()
            get_one = db.fetch_redflag(redflag_id)

            if username and get_one:
                db.delete_redflag(redflag_id)
                return jsonify({
                    'message': 'Redflag record deleted succesfully.',
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

    def update_status(self, redflag_id, data):
        """
        A method for updating status a specific redflag from the report.
        """
        try:
            get_one = db.fetch_redflag(redflag_id)
            if get_one:
                db.update_status(redflag_id, data)
                return jsonify({
                    'status': 200,
                    'data': db.fetch_redflag(redflag_id),
                    'message': 'Redflag status successfully updated!'
                                }), 200
            else:
                return jsonify({'status': 404,
                                'message': 'No such redflag record found!'
                                }), 404
        except ValueError:
            return jsonify({
                'status': 400,
                'message': 'Please provide right inputs'
            }), 400
  
    def update_location(self, redflag_id, data):
        """
        A method for updating location a specific redflag from the report.
        """
        location = data.get('location')
        try:
            get_one = db.fetch_redflag(redflag_id)
            if get_one:
                db.update_location(redflag_id, location)
                return jsonify({
                    'status': 200,
                    'data': db.fetch_redflag(redflag_id),
                    'message': 'Redflag location successfully updated!'
                                }), 200
            else:
                return jsonify({
                    'status': 404,
                    'message': 'No such redflag record found!'
                                }), 404
        except ValueError:
            return jsonify({
                'message': 'Please provide right inputs'
            }), 400

    def update_comment(self, redflag_id, data):
        """
        A method for updating a comment of a specific redflag from the report.
        """
        comment = data.get('comment')
        try:
            get_one = db.fetch_redflag(redflag_id)
            if get_one:
                db.update_comment(redflag_id, comment)
                return jsonify({'status': 200,
                                'data': db.fetch_redflag(redflag_id),
                                'message': 'Redflag comment successfully updated!'
                                }), 200
            else:
                return jsonify({'status': 404,
                                'message': 'No such redflag record found!'
                                }), 404
        except ValueError:
            return jsonify({
                'status': 400,
                'message': 'Please provide right inputs'
            }), 400