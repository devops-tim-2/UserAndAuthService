from common.database import db_session
from models.models import User
def create(user):
    db_session.add(user)
    db_session.commit()
    return user
    
def get_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

def get_by_id(id):
    user = User.query.get(id)
    return user