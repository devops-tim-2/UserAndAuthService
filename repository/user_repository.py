from common.database import db_session

def create(user):
    db_session.add(user)
    db_session.commit()
    return user