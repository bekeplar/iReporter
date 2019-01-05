from api.models import users, incidents
from flask_jwt_extended import get_jwt_identity


def get_user(current_user):
    """function returns data attached to the current user """
    for user in users:
        if user['email'] == current_user:
            return user


def check_is_admin(current_user):
    """function checks if a user is an admin """
    return current_user['isAdmin']


def create_user(username, password):
    """function to create a new user. """
    for user in users:
        if user.username == None:
            users.append(user)


def login_user(username):
    """function that allows a known user login """
    for user in users:
        if user.username == user['username']:
            return user['username']
    return None


def known_user():
    current_user = get_jwt_identity()
    current_user = get_user(current_user)
    return current_user


def verify_status(status):
    """function that verifies a status """
    keys = ['under investigation', 'rejected', 'resolved']
    for key in keys:
        if not key:
            return "Please add either 'resolved', 'rejected' or 'under investigation as status"
        
