from common.database import db_session
from models.models import FollowRequest

def exists(source, destination):
    return db_session.query(FollowRequest.query.filter(FollowRequest.src == source, FollowRequest.dst == destination).exists()).scalar()

def create(follow_request):
    db_session.add(follow_request)
    db_session.commit()
    return follow_request