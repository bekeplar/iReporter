import json
from database.db import DatabaseConnection
from api.controllers.user import UserController
from flask import request, Blueprint

user_blueprint = Blueprint('user blueprint', __name__)
db = DatabaseConnection()
user_controller = UserController()


@user_blueprint.route('/auth/signup', methods=['POST'])
def signup():
    """This function has a route used to create a new user."""
    data = json.loads(request.data)
    return user_controller.create_user(data)


@user_blueprint.route('/auth/login', methods=['POST'])
def login():
    """This function allows a registered user to login"""
    data = json.loads(request.data)
    return user_controller.signin_user(data)