
from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import User
from common.config import setup_config
import json

class TestRegistration:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        valid_user_data = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": True,"taggable": True }
        cls.valid_user = User(**valid_user_data, state='ACCEPTED')
        db_session.add(cls.valid_user)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_register_happy(self):
        valid_user_2_data = { "username": "user2","password": "password","role": "user","age": 24,"sex": "M","region": "eu","interests": "sport","bio": "test profile 2.","website": "http://www.google.com/","phone": "066345345","mail": "nenad2@misic.com","profile_image_link": "","public": True,"taggable": True }
        response = self.client.post('/api/register', data=json.dumps(valid_user_2_data), content_type='application/json')
        assert response.status_code == 200

    
    def test_register_sad(self):
        invalid_user_data = { "username": "user1","password": "password","role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropori i ostalo","bio": "test profile 3.","website": "http://www.google.com/","phone": "066345345","mail": "nenad@misic.com","profile_image_link": "","public": True,"taggable": True }
        response = self.client.post('/api/register', data=json.dumps(invalid_user_data), content_type='application/json')
        assert response.status_code == 400

    @classmethod
    def teardown_class(cls):
        from common.database import db_session
        db_session.rollback()