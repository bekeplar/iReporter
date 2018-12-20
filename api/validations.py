import re
from api.models import User, Incident


class UserValidation(User):

    def validate_input(self):
            if not self.firstname or self.firstname.isspace():
                return 'Please fill in firstname field!'
            elif not self.lastname or self.lastname.isspace():
                return'Please fill in lastname field!'
            elif not self.othernames or self.othernames.isspace():
                return'Please fill in othernames field!'
            if not self.username or self.username.isspace():
                return 'Please fill in username field!'    
            elif not self.email or self.email.isspace():
                return'Please fill in email field!'
            elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email):
                return 'Please fill in right email format!.'
            elif not self.password or self.password.isspace():
                return 'Plese fill in password field!'
            elif len(self.password) < 8:
                return 'Password must be of 8 characters long!'

    def login_validate(email, password):
        if not email or email.isspace():
            return 'Plese fill in email field!'
        elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", email):
            return 'Please fill in right email format!.'   
        elif not password or password.isspace():
            return 'Plese fill in password field!'
        else:
            return None


class IncidentValidation(Incident):

    def validate_input(self):
            if not self.title or self.title.isspace():
                return 'Please fill in title field!'
            elif not self.location or self.location.isspace():
                return'Please fill in location field!'
            elif not self.comment or self.comment.isspace():
                return'Please fill in the comments field!'
            elif not self.status or self.status.isspace():
                return 'Please select status!'
            else:
                return None