import unittest
from api.models.incident import incidents
from api import create_app
import json


class TestRedflag(unittest.TestCase):
    def setUp(self):
        """
        Setting up a test client
        """
        self.app = create_app('Testing')
        self.test_client = self.app.test_client()
        self.user = {
            "firstname": "bekelaze",
            "lastname": "Joseph",
            "othernames": "beka",
            "email": "bekeplar@gmail.com",
            "phoneNumber": "0789057968",
            "username": "bekeplar",
            "isAdmin": "False",
            "password": "bekeplar1234"
        }

        self.login_user = {
            'username': 'bekeplar',
            'password': 'bekeplar1234'
        }

        self.redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }

    def test_create_redflag(self):
        """
        Test if a user can create a redflag successfully.
        """

        response = self.test_client.post(
            'api/v1/signup',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['message'], "bekeplar successfully registered.")
        
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.login_user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        
        response = self.test_client.post(
            'api/v1/redflags',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        self.assertEqual(201, response.status_code)

    def test_create_redflag_twice(self):
        """
        Test if a user can create a redflag successfully.
        """
       
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
    
        response = self.test_client.post(
            'api/v1/redflags',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['Error'], 'Redflag record already reported!')
        self.assertEqual(406, response.status_code)

    def test_create_redflag_unauthorised_user(self):
        """
        Test if a non user can create a redflag successfully.
        """
        
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        self.assertEqual(401, response.status_code)

    def test_create_redflag_no_token(self):
        """
        Test if a user can create a redflag successfully.
        """
    
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        self.assertEqual(401, response.status_code)    

    def test_create_redflag_empty_createdBy(self):
        """
        Test if a user can create a redflag with missing createdBy.
        """
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "",
            "type": "redflag",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['Error'], 'Please fill in reporter field!')

    def test_create_redflag_empty_type(self):
        """
        Test if a user can be created with no type of incident.
        """
        
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())
        self.assertEqual(message['Error'], 'Please select incident type!')

    def test_create_redflag_empty_title(self):
        """
        check if a user can create a redflag with no title.
        """

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['Error'], 'Please fill in title field!')
        
    def test_create_redflag_empty_video(self):
        """
        check if a user can create a redflag with no video.
        """
    
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": ""
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )
        self.assertEqual(400, response.status_code)

    def test_create_redflag_empty_images(self):
        """
        check if a user can create a redflag with no images.
        """

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )
        self.assertEqual(400, response.status_code)

    def test_create_redflag_no_location(self):
        """
        check if a user can create a redflag with no location.
        """

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "",
            "comment": "corrupt traffic officers in mukono",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )
        message = json.loads(response.data.decode())
        self.assertEqual(message['Error'], 'Please fill in location field!')

    def test_create_redflag_no_comment(self):
        """
        check if a user can create a redflag with no comment.
        """
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        redflag = {
            "createdBy": "Bekalaze",
            "type": "redflag",
            "title": "corruption",
            "location": "1.33, 2.045",
            "comment": "",
            "status": "draft",
            "images": "nn.jpg",
            "videos": "nn.mp4"
        }
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(redflag)
        )

        message = json.loads(response.data.decode())
        self.assertEqual(message['Error'], 'Please fill in the comments field!')

    def test_get_all_redflags(self):
        """Test that a user can get all his created redflags"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        response = self.test_client.post(
            'api/v1/redflags',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            content_type='application/json'

        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'These are your reports!')
        self.assertEqual(200, response.status_code)

    def test_get_all_redflags_non_user(self):
        """Test that a non-user cannot get created redflags"""
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            data=json.dumps(self.redflag)
        )
        response = self.test_client.get(
            '/api/v1/redflags',
            content_type='application/json'
        )
        self.assertEqual(401, response.status_code)

    def test_get_specific_redflag_not_existing(self):
        """Test that a user cannot get a non existing redflag record"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        response = self.test_client.get(
            '/api/v1/redflags/1'
        )
        self.assertEqual(401, response.status_code)

    def test_get_specific_redflag_empty_list(self):
        """Test that a user cannot get a redflag from empty list"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        response = self.test_client.get(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' + access_token['token']}
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'],  'Redflag record found!' )

    def test_delete_specific_redflag(self):
        """Test that a user can delete a specific created redflags"""
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code) 
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        response = self.test_client.delete(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' + access_token['token']}
        )
        self.assertEqual(200, response.status_code)

    def test_delete_specific_redflag_not_existing(self):
        """Test that a user cannot delete a non existing redflag record"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        response = self.test_client.delete(
            '/api/v1/redflags/200',
            headers={'Authorization': 'Bearer ' + access_token['token']}
        )
        self.assertEqual(404, response.status_code)  

    def test_update_location_specific_redflag(self):
        """Test that a user can update location of a specific created redflag"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        new_location = {
            "location": "1.784, 4.0987"
        }

        response = self.test_client.patch(
            'api/v1/redflags/1/location',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        self.assertEqual(200, response.status_code)

    def test_edit_location_specific_redflag_non_existing(self):
        """Test that a user cannot update location for non existing redflag"""
  
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        new_location = {
            
            "location": "1.784, 4.0987"
        }

        response = self.test_client.patch(
            'api/v1/redflags/10000/location',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        self.assertEqual(404, response.status_code)

    def test_update_comment_specific_redflag(self):
        """Test that a user can update comment of a specific created redflag"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        new_location = { 
            "comment": "corruption is killing our systems"
        }

        response = self.test_client.patch(
            'api/v1/redflags/1/comment',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        self.assertEqual(200, response.status_code)

    def test_edit_comment_not_in_list(self):
        """Test that a user cannot update comment for non existing redflag"""
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        new_location = {
            "comment": "corruption is killing our systems"  
        }

        response = self.test_client.patch(
            'api/v1/redflags/10000/comment',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        self.assertEqual(404, response.status_code)

    def test_update_status_specific_redflag(self):
        """Test that a user can update comment of a specific created redflag"""

        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        new_location = { 
            "status": "resolved"
        }

        response = self.test_client.patch(
            'api/v1/redflags/1/status',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'Redflag status successfully updated!')
        self.assertEqual(200, response.status_code)

    def test_edit_status_not_in_list(self):
        """Test that a user cannot update comment for non existing redflag"""
   
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)
        new_location = {
            "status": "resolved"  
        }

        response = self.test_client.patch(
            'api/v1/redflags/10000/status',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        self.assertEqual(404, response.status_code)

    def test_update_status_specific_redflag_not_known_status(self):
        """Test that a user can update comment of a specific created redflag"""
    
        response = self.test_client.post(
            'api/v1/login',
            content_type='application/json',
            data=json.dumps(self.user)
        )
        access_token = json.loads(response.data.decode())
        self.assertEqual(200, response.status_code)

        response = self.test_client.post(
            'api/v1/redflags',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(self.redflag)
        )
        new_location = { 
            "status": "done"
        }

        response = self.test_client.patch(
            'api/v1/redflags/1/status',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' + access_token['token']},
            data=json.dumps(new_location)
        )
        reply = json.loads(response.data.decode())
        self.assertEqual(reply['message'], 'Redflag status successfully updated!')
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        """
        Destroying a test client
        """
        incidents.clear()