from database.db import DatabaseConnection

db = DatabaseConnection()


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

    def check_user_exist(self):
        username = db.check_username(self.username)
        email = db.check_email(self.email)
        if username != None:
            return 'Username is taken.'
        if email != None:
            return 'Email already has an account.'
