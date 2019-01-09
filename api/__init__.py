from flask import Flask, jsonify
import datetime
from instance.config import app_config
from api.views import blueprint
from flask_jwt_extended import JWTManager


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['JWT_SECRET_KEY'] = 'kimberley!'
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
    JWTManager(app)

    #  Register blueprints
    app.register_blueprint(blueprint, url_prefix='/api/v1')

    valid_urls = [
            "POST /api/v1/signup",
            "POST /api/v1/login",
            "GET /api/v1/redflags",
            "GET /api/v1 /redflags/<int:id>",
            "PATCH /api/v1/redflags/<int:id>/location",
            "PATCH /api/v1/redflags/<int:id>/status",
            "PATCH /api/v1/redflags/<int:id>/comment",
            "DELETE /api/v1/redflags/<int:id>Delete a redflag"
        ]

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            'Issue': 'You have entered an unknown URL.',
            'Valid URLs': valid_urls,
            'status': 404,
            'message': 'Please contact the Admin for more details on this API.'
            }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            'Issue': 'Method Not Allowed.',
            'Supported Methods': valid_urls,
            'status': 405,
            'message': 'Please follow this guide for details on this API.'
            }), 405

    return app

