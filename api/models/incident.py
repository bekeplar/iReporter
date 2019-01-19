from database.db import DatabaseConnection

db = DatabaseConnection()

incidents = []


class Incident:
    """This class contains all incident objects"""

    def __init__(self, *args):
        self.id = args[0]
        self.createdBy = args[1]
        self.type = args[2]
        self.title = args[3]
        self.location = args[4]
        self.comment = args[5]
        self.status = args[6]
        self.createdOn = args[7]
        self.images = args[8]
        self.videos = args[9]
    
    def check_incident_exist(self):
        title = db.check_title(self.title)
        comment = db.check_comment(self.comment)
        if title != None:
            return 'Title already reported.'
        if comment != None:
            return 'comment already reported.'

    
