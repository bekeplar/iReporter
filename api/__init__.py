from flask import Flask
import os
from instance.config import app_settings
from api.views import blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'kimberley!'

#  Register blueprints
app.register_blueprint(blueprint, url_prefix='/api/v1')
