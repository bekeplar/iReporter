from api.models import users
from database.db import DatabaseConnection

db = DatabaseConnection()


def check_editable_status(status):
    """
    Function to comfirm editable redflag status.
    """
    status = db.check_status(status)
    if status != 'draft':
        return 'Only draft status can be edited!'



