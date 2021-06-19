from models.models import AgentRequest, User
from service import user_service
import pytest

valid_user = { "username": "user1","password": "user","role": "user","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }
valid_agent = { "username": "agent1","password": "agent","role": "agent","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }
user_invalid_role = { "username": "user2","password": "user","role": "idk","age": 24,"sex": "M","region": "eu","interests": "sport, stiropor","bio": "test profile.","website": "http://www.google.com/","phone": "066345345","mail": "nenad@misic.com","profile_image_link": "https://tinypng.com/images/social/website.jpg","public": True,"taggable": True }


def test_register_okay_user(mocker):
    expected = User(**valid_user, state='ACCEPTED', id=-1)
    mocker.patch('service.user_service.user_repository.create', return_value=expected)
    mocker.patch('broker.produce.publish', return_value=None)
    actual = user_service.register_user(User(**valid_user, state='PENDING'))
    
    assert hasattr(actual, 'id')
    actual.id = -1
    expected.id = -1
    actual.password = 'password'
    expected.password = 'password'
    assert expected.get_dict()==actual.get_dict()

def test_register_okay_agent(mocker):
    expected = User(**valid_agent, state='PENDING', id=-1)
    expected_agent_request = AgentRequest(id=-1, u_id=-1)
    mocker.patch('service.user_service.user_repository.create', return_value=expected)
    mocker.patch('service.user_service.agent_request_repository.create', return_value=expected_agent_request)
    mocker.patch('broker.produce.publish', return_value=None)
    actual = user_service.register_user(User(**valid_agent, state='PENDING'))
    assert hasattr(actual, 'id')
    actual.id = -1
    expected.id = -1
    actual.password = 'password'
    expected.password = 'password'
    assert expected.get_dict()==actual.get_dict()

def test_register_no_role(mocker):
    with pytest.raises(Exception) as e_info:
        mocker.patch('service.user_service.user_repository.create', return_value=None)
        mocker.patch('broker.produce.publish', return_value=None)
        user_service.register_user(User(**user_invalid_role, state='PENDING'))