from common.database import db

def create(user):
    db.session.add(user)
    db.session.commit()

    return user