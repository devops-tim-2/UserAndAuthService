from exceptions.exceptions import NotAccessibleException
from broker.producer import publish
from models.models import AgentRequest, Follow, FollowRequest, User
from exceptions.exceptions import AlreadyFollowException, AlreadySentFollowRequestException, InvalidRoleException, InvalidCredentialsException, MissingUserException
from repository import user_repository, agent_request_repository, follow_request_repository, follow_repository
import bcrypt 

import time
from os import environ
import jwt

MESSAGE_USER_FOLLOW_CREATED = 'user.follow.created'
MESSAGE_AGENT_REQUEST_CREATED = 'agent.request.created'
MESSAGE_USER_CREATED = 'user.created'

def register_user(user:User) -> User:
    # Server validates sent data
    if user.role == 'agent':
        # Password is encrypted using bcrypt algorithm
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # User is saved to database with state set to PENDING
        user.state = 'PENDING'
        persisted_user = user_repository.create(user)
        # New entity is created in AgentRequest table with u_id pointing to created user id
        agent_request = AgentRequest(u_id=persisted_user.id)
        persisted_agent_request = agent_request_repository.create(agent_request)


        dt = persisted_user.get_dict()
        del dt['password']
        dt['agent_request_id'] = persisted_agent_request.id
        # agent.request.created event is sent to RabbitMQ
        publish(MESSAGE_AGENT_REQUEST_CREATED, dt)
        # If and when administrator approves registration request (when agent.request.approved event is catched), user state is set to ACCEPTED and user.created event is fired
        # If administrator rejects registration request (agent.request.rejected is catched), user state is set to REJECTED and no events are fired
    elif user.role == 'user':
        # Password is encrypted using bcrypt algorithm
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # User is saved to database with state set to ACCEPTED
        user.state = 'ACCEPTED'
        persisted_user = user_repository.create(user)
        dt = persisted_user.get_dict()
        del dt['password']
        # user.created event is sent to RabbitMQ
        publish(MESSAGE_USER_CREATED, dt)
    else:
        raise InvalidRoleException()

    return persisted_user

def login(username, password):
    user = user_repository.get_by_username(username)
    if not user:
        raise InvalidCredentialsException()

    real_password = user.password
    if bcrypt.checkpw(password.encode('utf-8'), real_password.encode('utf-8')):
        user_dict = user.get_dict()
        del user_dict['password']
        user_dict["iat"] = round(time.time() * 1000)
        user_dict["exp"] = round(time.time() * 1000) + 7200000 #2hours from now
        encoded_jwt = jwt.encode(user_dict, environ.get('JWT_SECRET'), algorithm=environ.get('JWT_ALGORITHM'))
        return encoded_jwt

    raise InvalidCredentialsException()


def follow(follow):
    src_user = user_repository.get_by_id(follow.src)
    dst_user = user_repository.get_by_id(follow.dst)

    if src_user is None or dst_user is None:
        raise MissingUserException()

    if follow_request_repository.exists(follow.src, follow.dst):
        raise AlreadySentFollowRequestException()
    if follow_repository.exists(follow.src, follow.dst):
        raise AlreadyFollowException()
        
    if not dst_user.public:
        if follow_request_repository.exists(follow.dst, follow.src):
            persisted_follow_src_dst = follow_repository.create(follow)
            persisted_follow_dst_src = follow_repository.create(Follow(src=follow.dst, dst=follow.src, mute=follow.mute))
            publish(MESSAGE_USER_FOLLOW_CREATED, persisted_follow_src_dst.get_dict())
            publish(MESSAGE_USER_FOLLOW_CREATED, persisted_follow_dst_src.get_dict())
            return "Handshake"
        elif follow_repository.exists(follow.dst, follow.src):
            persisted_follow = follow_repository.create(follow)
            publish(MESSAGE_USER_FOLLOW_CREATED, persisted_follow.get_dict())
            return "Followback"
        else:
            follow_request_repository.create(FollowRequest(src=follow.src, dst=follow.dst, mute=follow.mute))
            return "Request"
    else:
        persisted_follow = follow_repository.create(follow)
        publish(MESSAGE_USER_FOLLOW_CREATED, persisted_follow.get_dict())
        return "Publicfollow"



def get_by_id(profile_id: int, user: dict):
    profile = user_repository.get_by_id(profile_id)

    # if not profile or (user and block_service.find(user['id'], profile_id)):
    #     raise NotFoundException(f'Profile with id {profile_id} not found.')

    pd = profile.get_dict()
    del pd['password']
    return pd