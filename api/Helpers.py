from api.models import users


def check_is_admin(current_user):
    """function checks if a user is an admin """
    return current_user['isAdmin']


def verify_status(status):
    """function that verifies a status """
    keys = ['under investigation', 'rejected', 'resolved']
    for key in keys:
        if not key:
            return "Please add either 'resolved', 'rejected' or 'under investigation as status"


