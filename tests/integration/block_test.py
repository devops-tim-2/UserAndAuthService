from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import Block,  User
from common.config import setup_config
import json

class TestBlock:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        account_1 = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": True,"taggable": True }
        account_2 = { "username": "user2","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad2@misic.com","profile_image_link": "","public": True,"taggable": True }
        cls.account_1 = User(**account_1, state='ACCEPTED')
        cls.account_2 = User(**account_2, state='ACCEPTED')
        db_session.add(cls.account_1)
        db_session.add(cls.account_2)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_block_happy(self):
        #self.private_1
        user = { "username": self.account_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        block = {'dst': self.account_2.id}
        response = self.client.post('/api/block', data=json.dumps(block), headers={"Authorization": f"Bearer {token}"}, content_type='application/json')
        assert response.status_code == 200
        assert response.get_json()['blocked'] == True
        

    def test_block_sad(self):
        block = { "dst": self.account_2.id}
        response = self.client.post('/api/block', data=json.dumps(block), content_type='application/json')
        assert response.status_code == 403
    

    @classmethod
    def teardown_class(cls):
        from common.database import db_session
        db_session.rollback()
        