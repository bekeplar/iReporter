from api.models import Incident, User
import re


class Validators(Incident):
    def validate_inputs(self):
        if not self.title or self.title.isspace():
            return 'Please fill in title field!'
        elif not self.location or self.location.isspace():
            return'Please fill in location field!'
        elif not self.type or self.type.isspace():
            return'Please select incident type!'
        elif not self.createdBy or self.createdBy.isspace():
            return'Please fill in reporter field!'
        elif not self.comment or self.comment.isspace():
            return'Please fill in the comments field!'
        else:
            return None

    def add_media(self):
        if not self.images or self.images.isspace():
            return 'Please add images for proof!'
        elif not self.videos or self.videos.isspace():
            return'Please add videos for proof!'
        else:
            return None        


class Validation(User):
    def validate_input(self):
        error = None
        if not self.firstname or self.firstname.isspace():
            error = 'Please fill in firstname field!'
        elif not self.lastname or self.lastname.isspace():
            error = 'Please fill in lastname field!'
        elif not self.othernames or self.othernames.isspace():
            error = 'Please fill in othernames field!'
        if not self.username or self.username.isspace():
            error = 'Please fill in username field!' 
        if not self.isAdmin or self.isAdmin.isspace():
            error = 'Please select user role!'    
        return error

    def validate_inputs(self):
        errors = None
        if not self.email or self.email.isspace():
            errors = 'Please fill in email field!'
        elif not self.phoneNumber or self.phoneNumber.isspace():
            errors = 'Please fill in phoneNumber field!'
        elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email):
            errors = 'Please fill in right email format!.'
        elif not self.password or self.password.isspace():
            errors = 'Plese fill in password field!'
        elif len(self.password) < 8:
            errors = 'Password must be of 8 characters long!'
        return errors

    @staticmethod
    def login_validate(username, password):
        if not username or username.isspace():
            return 'Please fill in username field!'
        elif not password or password.isspace():
            return 'Please fill in password field!'
        elif len(password) < 8:
            return 'Password must be of 8 characters long!'
        return None
