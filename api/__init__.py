from flask import Flask
from api.views import blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'kimberley!'
app.register_blueprint(blueprint, url_prefix='/api/v1')
