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

    @app.errorhandler(404)
    def page_not_found(e):
        valid_urls = [
            "POST/signup",
            "POST/login",
            "GET /redflags",
            "GET /redflags/<id>",
            "PATCH /redflags/<id>/location",
            "PATCH /redflags/<id>/",
            "PATCH /redflags/<id>/comment",
            "DELETE /redflags/<id>Delete a redflag"
        ]
        return jsonify({
            'Issue': 'You have entered an unknown URL.',
            'Valid URLs': valid_urls,
            'status': 404,
            'message': 'Please contact the Admin for more details on this API.'
            }), 404
    return app

