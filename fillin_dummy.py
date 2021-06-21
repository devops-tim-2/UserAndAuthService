from models.models import User
from common.database import db_session

PASSWORD = b"$2b$12$56eVjoYbq6WrrafBYfNWqOZkMNHkzPbri4sZUVNLwpfS/vnobdKTa"

user1_public = User(username="user1", password=(PASSWORD).decode('utf-8'), role="user", age=24,sex="M", region="eu", interests="sport", bio="test profile 1.", website="http://www.google.com/", phone="066345345", mail="user1@mail.com", profile_image_link="", public=True, taggable=True, state='ACCEPTED')
user2_public = User(username="user2", password=(PASSWORD).decode('utf-8'), role="user", age=24,sex="M", region="eu", interests="sport, stiropor", bio="test profile 2.", website="http://www.google.rs/", phone="066345345", mail="user2@mail.com", profile_image_link="", public=True, taggable=True, state='ACCEPTED')
user3_private = User(username="user3", password=(PASSWORD).decode('utf-8'), role="user", age=24,sex="M", region="eu", interests="sport, stiropor, matematika", bio="test profile 3.", website="http://www.google.it/", phone="066345345", mail="user3@mail.com", profile_image_link="", public=False, taggable=True, state='ACCEPTED')
user4_private = User(username="user4", password=(PASSWORD).decode('utf-8'), role="user", age=24,sex="M", region="eu", interests="sport, stiropor, sve lepo", bio="test profile 4.", website="http://www.google.ba/", phone="066345345", mail="user4@mail.com", profile_image_link="", public=False, taggable=True, state='ACCEPTED')

db_session.add(user1_public)
db_session.add(user2_public)
db_session.add(user3_private)
db_session.add(user4_private)
db_session.commit()