

class User:
    users = []
    """ A class stores user object details """
    def __init__(self, *args):
        self.firstname = args[0]
        self.lastname = args[1]
        self.othernames = args[2]
        self.email = args[3]
        self.phoneNumber = args[4]
        self.username = args[5]
        self.registered = args[6]
        self.isAdmin = args[7]
        self.password = args[8]

    def create_user(self, username, password):
        for user in self.users:
            if user.username == None:
                self.users.append(user)

    def check_user_exist(self, email, username):
        for user in self.users:
            if self.username != None:
                return 'username already taken!'
            if self.email != None:
                return 'Email already has an account!'


class Incident:
    incidents = []
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

    def check_incident_exist(self, title):
        for incident in self.incidents:
            if incident.title != None:
                return 'Incident already reported!'

               

    
