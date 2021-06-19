from models.models import User
from common.config import setup_config
import json


class TestUser:
    @classmethod
    def setup_class(cls):
        cls.app, cls.db = setup_config('test')
        # user1 : password
        valid_user_data = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }
        cls.valid_user = User(**valid_user_data, state='ACCEPTED')
        cls.db.session.add(cls.valid_user)
        cls.db.session.commit()

        cls.client = cls.app.test_client()


    def test_register_happy(self):
        valid_user_2_data = { "username": "user2","password": "password","role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad2@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }
        response = self.client.post('/api/register', data=json.dumps(valid_user_2_data), content_type='application/json')
        assert response.status_code == 200
    
    def test_register_sad(self):
        invalid_user_data = { "username": "user1","password": "password","role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }
        response = self.client.post('/api/register', data=json.dumps(invalid_user_data), content_type='application/json')
        assert response.status_code == 400
