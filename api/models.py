users = []


class User:
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

