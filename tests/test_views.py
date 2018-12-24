import unittest
from api.models import User, Incident
from api import app
import json


class TestUser(unittest.TestCase):
    def setUp(self):
        """
        Setting up a test client
        """
        self.test_client = app.test_client()

    def test_create_user(self):
        """
        Test if a user can be registered successfully.
        """
        user = {
            "firstname": "bekelaze",
            "lastname":" Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], "bekeplar successfully registered.")

    def test_home(self):
        response = self.test_client.get(
            '/api/v1/'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], "Welcome to bekeplar's iReporter app.")
        self.assertEqual(response.status_code, 200)


    def test_create_user_empty_username(self):
        """
        Test if a user can be created with empty username.
        """
        user = {
            "firstname": "bekelaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in username field!')

    def test_create_user_empty_firstname(self):
        """
        Test if a user can be created with no firstname.
        """
        user = {
            "firstname": "",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in firstname field!')

    def test_create_user_empty_lastname(self):
        """
        Test if a user can be created with no lastname.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in lastname field!')

    def test_create_user_empty_othernames(self):
        """
        Test if a user can be created with no othernames.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in othernames field!')

    def test_create_user_empty_email(self):
        """
        Test if a user can be created with no email.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in email field!')
    
    def test_create_user_wrong_email_format(self):
        """
        Test if a user can be created with invalid email.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "nnnnnnnnnnn",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in right email format!.')

    def test_create_user_empty_phoneNumber(self):
        """
        Test if a user can be created with no phone Number.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in phoneNumber field!')

    def test_create_user_empty_isAdmin(self):
        """
        Test if a user can be created with no role selected.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "",
            "password": "bekeplar1234"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please select user role!')

    def test_create_user_empty_password(self):
        """
        Test if a user can be created with no password.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": ""
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Plese fill in password field!')

    def test_create_user_invalid_password_length(self):
        """
        Test if a user can be created with short password.
        """
        user = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "beka"
        }

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Password must be of 8 characters long!')


class TestRedflag(unittest.TestCase):
    def setUp(self):
        """
        Setting up a test client
        """
        self.test_client = app.test_client()

    def test_create_redflag(self):
        """
        Test if a user can create a redflag successfully.
        """
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['message'], 'created redflag reccord!')

    def test_create_redflag_empty_createdBy(self):
        """
        Test if a user can create a redflag with missing createdBy.
        """
        redflag = {
            "createdBy": "",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in reporter field!')

    def test_create_redflag_empty_type(self):
        """
        Test if a user can be created with no type of incident.
        """
        redflag = {
            "createdBy": "Bekalaze",
            "type": "",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please select incident type!')

    def test_create_redflag_empty_title(self):
        """
        check if a user can create a redflag with no title.
        """
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in title field!')
        

    def test_create_redflag_no_location(self):
        """
        check if a user can create a redflag with no location.
        """
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in location field!')

    def test_create_redflag_no_comment(self):
        """
        check if a user can create a redflag with no comment.
        """
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())

        self.assertEqual(message['Error'], 'Please fill in the comments field!')
 
    def test_get_all_redflags(self):
        """Test that a user can get all his created redflags"""
        response = self.test_client.get(
            '/api/v1/redflags'
        )

        reply = json.loads(response.data.decode())

        self.assertEqual(reply['message'], 'These are your reports!')
        self.assertEqual(response.status_code, 200)


    def test_get_specific_redflag(self):
        """Test that a user can get a specific created redflags"""
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )
        response = self.test_client.get(
            '/api/v1/redflags/1'
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'Redflag record found!')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_redflag_not_existing(self):
        """Test that a user cannot get a non existing redflag record"""
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )
        response = self.test_client.get(
            '/api/v1/redflags/2'
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'No such redflag record found!')
        self.assertEqual(response.status_code, 200)

    def test_delete_specific_redflag(self):
        """Test that a user can delete a specific created redflags"""
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )
        response = self.test_client.delete(
            '/api/v1/redflags/1'
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'Redflag record  deleted!')
        self.assertEqual(response.status_code, 200)

    def test_delete_specific_redflag_not_existing(self):
        """Test that a user cannot delete a non existing redflag record"""
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "mukono",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft"
        }

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(redflag)
        )
        response = self.test_client.delete(
            '/api/v1/redflags/2'
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'No such redflag record found!')
        self.assertEqual(response.status_code, 200)
    

    def test_update_location_specific_redflag(self):
        """Test that a user can update location of a specific created redflag"""
        new_location = {
            
            "location": "kampala"
        }

        response = self.test_client.patch(
            'api/v1/redflags/1/location',
            content_type='application/json',
            data=json.dumps(new_location)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'],'Redflag location successfully updated!')
        self.assertEqual(response.status_code, 200)


        def test_update_location_specific_redflag_non_existing(self):
            """Test that a user cannot update location for non existing redflag"""
        new_location = {
            
            "location": "kampala"
        }

        response = self.test_client.patch(
            'api/v1/redflags/10000/location',
            content_type='application/json',
            data=json.dumps(new_location)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'No such redflag record found!')
        self.assertEqual(response.status_code, 404)


        
