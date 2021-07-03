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

def update(user_id, username, age, sex, region, interests, bio, website, phone, profile_image_link, public, taggable):
    user = User.query.get(user_id)
    user.username = username if username else user.username
    user.age = age if age else user.age
    user.sex = sex if sex else user.sex
    user.region = region if region else user.region
    user.interests = interests if interests else user.interests
    user.bio = bio if bio else user.bio
    user.website = website if website else user.website
    user.phone = phone if phone else user.phone
    user.profile_image_link = profile_image_link if profile_image_link else user.profile_image_link
    user.public = public if public else user.public
    user.taggable = taggable if taggable else user.taggable
    db_session.commit()
    return user


def delete(user_id):
    user = User.query.filter(User.id == user_id).first()
    db_session.delete(user)
    db_session.commit()