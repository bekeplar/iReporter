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
        elif not self.status or self.status.isspace():
            return 'Please select draft as status!'
        else:
            return None
 

class Validation(User):
    def validate_input(self):
        if not self.firstname or self.firstname.isspace():
            return 'Please fill in firstname field!'
        elif not self.lastname or self.lastname.isspace():
            return'Please fill in lastname field!'
        elif not self.othernames or self.othernames.isspace():
            return'Please fill in othernames field!'
        if not self.username or self.username.isspace():
            return 'Please fill in username field!' 
        if not self.isAdmin or self.isAdmin.isspace():
            return 'Please select user role!'    
        elif not self.email or self.email.isspace():
            return'Please fill in email field!'
        elif not self.phoneNumber or self.phoneNumber.isspace():
            return'Please fill in phoneNumber field!'
        elif not re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email):
            return 'Please fill in right email format!.'
        elif not self.password or self.password.isspace():
            return 'Plese fill in password field!'
        elif len(self.password) < 8:
            return 'Password must be of 8 characters long!'
