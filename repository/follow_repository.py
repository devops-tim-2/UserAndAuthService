from common.database import db_session
from models.models import Follow

def get(source, destination):
    return Follow.query.filter(Follow.src == source, Follow.dst == destination).first()

def exists(source, destination):
    return db_session.query(Follow.query.filter(Follow.src == source, Follow.dst == destination).exists()).scalar()

def create(follow):
    db_session.add(follow)
    db_session.commit()
    return follow

def mute(follow, mute_status):
    follow.mute = mute_status
    db_session.commit()
    return follow