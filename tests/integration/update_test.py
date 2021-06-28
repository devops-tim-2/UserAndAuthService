
from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import User
from common.config import setup_config
import json

class TestUpdate:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        valid_user_data = { "username": "user122","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": True,"taggable": True }
        cls.valid_user = User(**valid_user_data, state='ACCEPTED')
        db_session.add(cls.valid_user)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_update_happy(self):

        user = { "username": self.valid_user.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        cjanged_data = { "username": "user123","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"age": 29,"sex": "F","region": "na","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad333@misic.com","profile_image_link": "","public": False,"taggable": False }
        
        response = self.client.put(f'/api/{self.valid_user.id}', data=json.dumps(cjanged_data), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200

    
    def test_update_sad(self):
        cjanged_data = { "username": "user123","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"age": 29,"sex": "F","region": "na","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad333@misic.com","profile_image_link": "","public": False,"taggable": False }
        response = self.client.put(f'/api/{self.valid_user.id}', data=json.dumps(cjanged_data), content_type='application/json')
        assert response.status_code == 403


    @classmethod
    def teardown_class(cls):
        from common.database import db_session
        db_session.rollback()