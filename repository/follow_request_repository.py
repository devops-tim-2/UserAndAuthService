from common.database import db_session
from models.models import FollowRequest

def get(source, destination):
    return FollowRequest.query.filter(FollowRequest.src == source, FollowRequest.dst == destination).first()

def exists(source, destination):
    return db_session.query(FollowRequest.query.filter(FollowRequest.src == source, FollowRequest.dst == destination).exists()).scalar()

def create(follow_request):
    db_session.add(follow_request)
    db_session.commit()
    return follow_request

def delete(source, destination):
    fr = FollowRequest.query.filter(FollowRequest.src == source, FollowRequest.dst == destination).first()
    db_session.delete(fr)
    db_session.commit()

def get_by_dst(destination):
    return FollowRequest.query.filter(FollowRequest.dst == destination)

def delete_with_user(user_id):
    FollowRequest.query.filter(FollowRequest.src == user_id).delete()
    FollowRequest.query.filter(FollowRequest.dst == user_id).delete()
    db_session.commit()