from api.models.user import users
from flask import jsonify
from api.models.incident import incidents
from werkzeug.security import check_password_hash


def check_is_admin(current_user):
    """function checks if a user is an admin """
    return current_user['isAdmin']


def create_user(username, password):
    """function to create a new user. """
    for user in users:
        if user.username == None:
            users.append(user)


def login_user(username, password):
    """function that allows a known user login """
    for user in users:
        if user.username == user['username'] and check_password_hash(user["password"], password):
            return True
    return False


def verify_status(status):
    """function that verifies a status """
    keys = ['under investigation', 'rejected', 'resolved']
    for key in keys:
        if not key:
            return "Please add either 'resolved', 'rejected' or 'under investigation as status"


def check_status():
    """function that checks the current status """
    redflagId = id
    for redflag in incidents:
        if int(redflag['id']) == redflagId:
            if redflag['status'] != 'draft':
                return True
        return False


