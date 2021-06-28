from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import Follow, User
from common.config import setup_config
import json

class TestMute:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        account_1 = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": True,"taggable": True }
        account_2 = { "username": "user2","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad2@misic.com","profile_image_link": "","public": True,"taggable": True }
        account_3 = { "username": "user3","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad3@misic.com","profile_image_link": "","public": True,"taggable": True }
        follow_1_2 = { "src": 1, "dst": 2, "mute": False}
        cls.account_1 = User(**account_1, state='ACCEPTED')
        cls.account_2 = User(**account_2, state='ACCEPTED')
        cls.account_3 = User(**account_3, state='ACCEPTED')
        cls.follow_1_2 = Follow(**follow_1_2)
        db_session.add(cls.account_1)
        db_session.add(cls.account_2)
        db_session.add(cls.account_3)
        db_session.add(cls.follow_1_2)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_mute_unmute(self):
        #self.private_1
        user = { "username": self.account_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        response = self.client.get(f'/api/follow/mute/{self.account_2.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.get_json()['muted'] == True
        response = self.client.get(f'/api/follow/mute/{self.account_2.id}', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.get_json()['muted'] == False
        

    def test_no_follow(self):
        #self.private_3
        user = { "username": self.account_3.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        response = self.client.get('/api/follow/mute/2', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400

    