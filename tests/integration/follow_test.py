from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import User
from common.config import setup_config
import json

class TestFollow:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        private_account_1 = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": False,"taggable": True }
        private_account_2 = { "username": "user2","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad2@misic.com","profile_image_link": "","public": False,"taggable": True }
        public_account_1 = { "username": "user3","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad3@misic.com","profile_image_link": "","public": True,"taggable": True }
        cls.private_1 = User(**private_account_1, state='ACCEPTED')
        cls.private_2 = User(**private_account_2, state='ACCEPTED')
        cls.public_1 = User(**public_account_1, state='ACCEPTED')
        db_session.add(cls.private_1)
        db_session.add(cls.private_2)
        db_session.add(cls.public_1)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_follow_priv_to_priv(self):
        #self.private_1
        user = { "username": self.private_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        follow = { "dst": self.private_2.id, "mute":False }
        response = self.client.post('/api/follow', data=json.dumps(follow), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200
        assert response.get_json()['state'] == 'Request'
        
        #self.private_2
        user_2 = { "username": self.private_2.username,"password": "password"}
        login_2 = self.client.post('/api/login', data=json.dumps(user_2), content_type='application/json')
        assert login_2.status_code == 200
        token_2 = login_2.get_json()['token']
        followback = { "dst": self.private_1.id, "mute":False }
        response_2 = self.client.post('/api/follow', data=json.dumps(followback), headers={"Authorization": f"Bearer {token_2}"}, content_type='application/json')
        assert response_2.status_code == 200
        assert response_2.get_json()['state'] == 'Handshake'

    def test_follow_priv_to_pub(self):
        #self.private_1
        user = { "username": self.private_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        follow = { "dst": self.public_1.id, "mute":False }
        response = self.client.post('/api/follow', data=json.dumps(follow), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200
        assert response.get_json()['state'] == 'Request'

    def test_follow_pub_to_priv(self):
        #self.public_1
        user = { "username": self.public_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        follow = { "dst": self.private_2.id, "mute":False }
        response = self.client.post('/api/follow', data=json.dumps(follow), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200
        assert response.get_json()['state'] == 'Request'

    def test_follow_pub_to_priv_already_follow(self):
        #self.public_1
        user = { "username": self.public_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        follow = { "dst": self.private_1.id, "mute":False }
        response = self.client.post('/api/follow', data=json.dumps(follow), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200
        assert response.get_json()['state'] == 'Handshake'

    
    def test_follow_sad(self):
        #no user
        follow = { "dst": self.public_1.id, "mute":False }
        response = self.client.post('/api/follow', data=json.dumps(follow), content_type='application/json')
        assert response.status_code == 403


    @classmethod
    def teardown_class(cls):
        from common.database import db_session
        db_session.rollback()