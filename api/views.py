import datetime
from flask import Flask, jsonify, request
from flask import Blueprint
from api.models import User, Incident
from api.validations import UserValidation, IncidentValidation


blueprint = Blueprint('application', __name__)


@blueprint.route('/')
def home():
    """A welcoming route to my api"""

    return jsonify({
        'message': 'Welcome to bekeplar\'s iReporter app.',
        'status': '200'
    }), 200
