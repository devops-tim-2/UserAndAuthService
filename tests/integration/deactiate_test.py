from os import environ
environ['SQLALCHEMY_DATABASE_URI'] = environ.get("TEST_DATABASE_URI")

from models.models import Block,  User
from common.config import setup_config
import json

class TestDeactivate:
    @classmethod
    def setup_class(cls):
        cls.app = setup_config('test')
        from common.database import db_session
        # user1 : password
        account_1 = { "username": "user1","password": (b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa").decode('utf-8'),"role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor, sve lepo","bio": "test profile 1.","website": "http://www.google.com/","phone": "066345345","mail": "nenad1@misic.com","profile_image_link": "","public": True,"taggable": True }
        cls.account_1 = User(**account_1, state='ACCEPTED')
        db_session.add(cls.account_1)
        db_session.commit()

        cls.client = cls.app.test_client()


    def test_deactivate_happy(self):
        user = { "username": self.account_1.username,"password": "password"}
        login = self.client.post('/api/login', data=json.dumps(user), content_type='application/json')
        assert login.status_code == 200
        token = login.get_json()['token']
        response = self.client.delete(f"/api/{self.account_1.id}", headers={"Authorization": f"Bearer {token}"})
        print(response.get_json())
        assert response.status_code == 200
        

    def test_deactivate_sad(self):
        response = self.client.delete(f"/api/{self.account_1.id}")
        assert response.status_code == 403

    @classmethod
    def teardown_class(cls):
        from common.database import db_session
        db_session.rollback()
        