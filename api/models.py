import datetime


class User:
    """ A class stores user object details """
    def __init__(self, **kwargs):
        self.firstname = kwargs.get("firstname")
        self.lastname = kwargs.get("lastname")
        self.othernames = kwargs.get("othernames")
        self.email = kwargs.get("email")
        self.phoneNumber = kwargs.get("phoneNumber")
        self.username = kwargs.get("username")
        self.registered = str(datetime.today().strftime("%d/%m/%Y"))
        self.isAdmin = False
        self.password = kwargs.get("password")

        self.users = []

    def check_user_exist(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user


class Incident:
    """This class contains all incident objects"""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.createdBy = kwargs.get("createdBy")
        self.title = kwargs.get('title')
        self.location = kwargs.get('location')
        self.comment = kwargs.get('comment')
        self.status = kwargs.get('status')
        self.createdOn = str(datetime.today().strftime("%d/%m/%Y"))
        self.incidents = []

    def check_incident_exist(self, id):
            for incident in self.incidents:
                if incident.id == id:
                    return incident