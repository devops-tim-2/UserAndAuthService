from exceptions.exceptions import NotAccessibleException, NotFoundException
from broker.producer import publish
from models.models import AgentRequest, Follow, FollowRequest, User
from exceptions.exceptions import AlreadyFollowException, AlreadySentFollowRequestException, InvalidRoleException, InvalidCredentialsException, MissingUserException, DoesNotFollowException
from repository import user_repository, agent_request_repository, follow_request_repository, follow_repository, block_repository
import bcrypt 

import time
from os import environ
import jwt

MESSAGE_USER_FOLLOW_CREATED = 'user.follow.created'
MESSAGE_USER_FOLLOW_DELETED = 'user.follow.deleted'
MESSAGE_AGENT_REQUEST_CREATED = 'agent.request.created'
MESSAGE_USER_CREATED = 'user.created'
MESSAGE_USER_UPDATED = 'user.updated'
MESSAGE_USER_BLOCK_CREATED = 'user.block.created'
MESSAGE_USER_BLOCK_DELETED = 'user.block.deleted'
MESSAGE_USER_FOLLOW_MUTE = 'user.follow.updated'

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
        follow_persistent = follow_repository.get(follow.src, follow.dst)
        follow_id = follow_persistent.id
        follow_repository.delete(follow.src, follow.dst)
        publish(MESSAGE_USER_FOLLOW_DELETED, follow_id)
        return 'Unfollow'
        
    if dst_user.public and src_user.public:
        persisted_follow = follow_repository.create(follow)
        publish(MESSAGE_USER_FOLLOW_CREATED, persisted_follow.get_dict())
        return "Publicfollow"
    else:
        if follow_request_repository.exists(follow.dst, follow.src):
            persisted_follow_src_dst = follow_repository.create(follow)
            persisted_follow_dst_src = follow_repository.create(Follow(src=follow.dst, dst=follow.src, mute=follow.mute))
            follow_request_repository.delete(follow.dst, follow.src)
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


def block(block):
    src_user = user_repository.get_by_id(block.src)
    dst_user = user_repository.get_by_id(block.dst)

    if src_user is None or dst_user is None:
        raise MissingUserException()

    if follow_request_repository.exists(block.src, block.dst):
        raise AlreadySentFollowRequestException()
    if follow_repository.exists(block.src, block.dst):
        raise AlreadyFollowException()
        
    if block_repository.exists(block.src, block.dst):
        block_id = block.id
        block_repository.delete(block)
        publish(MESSAGE_USER_BLOCK_DELETED, block_id)
        return False
    else:
        persisted_block = block_repository.create(block)
        publish(MESSAGE_USER_BLOCK_CREATED, persisted_block.get_dict())
        return True
   


def get_follow(src, dst):
    if follow_repository.exists(src, dst):
        follow = follow_repository.get(src,dst)
        return follow, 'ACCEPTED'
    elif follow_request_repository.exists(src,dst):
        follow = follow_request_repository.get(src,dst)
        return follow, 'PENDING'
    raise NotFoundException()


def mute(src, dst):
    if follow_repository.exists(src, dst):
        follow = follow_repository.get(src,dst)
        current_mute_status = follow.mute
        follow_persistent = follow_repository.mute(follow, not(current_mute_status))
        publish(MESSAGE_USER_FOLLOW_MUTE, follow_persistent.get_dict())
        return follow_persistent.mute

    raise DoesNotFollowException()


def get_by_id(profile_id: int, user: dict):
    if not(user is None) and block_repository.exists(user['id'], profile_id):
        raise NotFoundException()

    profile = user_repository.get_by_id(profile_id)

    pd = profile.get_dict()
    del pd['password']
    return pd

def get_follow_requests(dst):
    return follow_request_repository.get_by_dst(dst)


def update(user_id, username, age, sex, region, interests, bio, website, phone, profile_image_link, public, taggable):
    persisted_user = user_repository.update(user_id, username, age, sex, region, interests, bio, website, phone, profile_image_link, public, taggable)
    dt = persisted_user.get_dict()
    if 'password' in dt: 
        del dt['password']
    # user.created event is sent to RabbitMQ
    publish(MESSAGE_USER_UPDATED, dt)

    return persisted_user

def delete(user_id):
    user = user_repository.get_by_id(user_id)

    if not user:
        raise NotFoundException()
    
    block_repository.delete_with_user(user_id)
    follow_repository.delete_with_user(user_id)
    follow_request_repository.delete_with_user(user_id)

    user_repository.delete(user_id)
    publish('user.deleted', user_id)


def approve(user_id: int):
    user_repository.approve(user_id)


def reject(user_id: int):
    user_repository.reject(user_id)
