import unittest
from database.db import DatabaseConnection
from api import create_app
import json


class TestUser(unittest.TestCase):
    def setUp(self):
        """
        Setting up a test client
        """
        self.db = DatabaseConnection()
        self.app = create_app('Testing')
        self.test_client = self.app.test_client()
        self.user1 = {
            "firstname": "bekelaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        self.user2 = {
            "firstname": "Nanyonjo",
            "lastname": "Favour",
            "othernames": "sylvia",
            "email": "nanyofav@gmail.com",
            "phoneNumber": "0789057968",
            "username": "favor",
            "isAdmin": "False",
            "password": "favor123"
        }

        self.user = {
            'username': 'bekeplar',
            'password': 'bekeplar1234'
        }
   
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['Error'], 'Please fill in username field!')

    def test_create_user(self):
        """
        Test if a user can be registered successfully.
        """
        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(message['message'], 'favor successfully registered.')

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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['Error'], 'Password must be of 8 characters long!')

    def test_user_login(self):
        """
        Test login a user successfully.
        """

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(self.user1)
        )

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(message['message'], 'bekeplar successfully logged in.')   

    def test_user_login_empty_username(self):
        """
        Test user login with empty username
        """
        user1 = {
            "firstname": "bekelaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )
        user = {
            'username': '',
            'password': 'bekeplar1234'
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['Error'], 'Please fill in username field!')

    def test_user_login_empty_password(self):
        """
        Test user login with empty password
        """
        user1 = {
            "firstname": "bekelaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": ""
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': 'bekeplar',
            'password': ''
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['Error'], 'Please fill in password field!')    

    def test_user_login_empty_fields(self):
        """
        Test user login with empty fields
        """
        user1 = {
            "firstname": "bekelaze",
            "lastname":" Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(user1)
        )

        user = {
            'username': '',
            'password': ''
        }

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(user)
        )

        message = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(message['Error'], 'Please fill in username field!')

    def tearDown(self):
        """
        Drop the user table very after a single test has run
        """
        self.db.drop_tables()
