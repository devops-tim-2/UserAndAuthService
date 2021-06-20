from flask_restful import Resource, reqparse
from service import user_service
from models.models import User

dto_parser = reqparse.RequestParser()
dto_parser.add_argument('username', type=str, help='Username for user account')
dto_parser.add_argument('password', type=str, help='Password for user account')
dto_parser.add_argument('role', type=str, help='Role for user account')
dto_parser.add_argument('age', type=int, help='Age for user account')
dto_parser.add_argument('sex', type=str, help='Sex for user account')
dto_parser.add_argument('region', type=str, help='Region for user account')
dto_parser.add_argument('interests', type=str, help='Interests for user account')
dto_parser.add_argument('bio', type=str, help='Bio for user account')
dto_parser.add_argument('website', type=str, help='Website for user account')
dto_parser.add_argument('phone', type=str, help='Phone for user account')
dto_parser.add_argument('mail', type=str, help='Email for user account')
dto_parser.add_argument('profile_image_link', type=str, help='Profile image link for user account')
dto_parser.add_argument('public', type=bool, help='Is profile public?')
dto_parser.add_argument('taggable', type=bool, help='Is profile taggable?')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, help='Username for user account')
login_parser.add_argument('password', type=str, help='Password for user account')

follow_parser = reqparse.RequestParser()
follow_parser.add_argument('src', type=str, help='Source of follow')
follow_parser.add_argument('dst', type=str, help='Destination of follow')
follow_parser.add_argument('mute', type=bool, help='Did the source mute the destination?')

block_parser = reqparse.RequestParser()
block_parser.add_argument('src', type=str, help='Source of follow')
block_parser.add_argument('dst', type=str, help='Destination of follow')

agent_request_parser = reqparse.RequestParser()
agent_request_parser.add_argument('u_id', type=int, help='Agent entity id')

class UserResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def get(self, user_id):
        # To be implemented.
        pass

    def put(self, user_id):
        # To be implemented.
        pass

    def delete(self, user_id):
        # To be implemented.
        pass

class UserListResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def post(self):
        # To be implemented.
        pass

class LoginResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def post(self):
        # To be implemented.
        pass

class RegisterResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def post(self):
        args = dto_parser.parse_args()
        user = User(
            username=args['username'],
            password=args['password'],
            role=args['role'],
            age=args['age'],
            sex=args['sex'],
            region=args['region'],
            interests=args['interests'],
            bio=args['bio'],
            website=args['website'],
            phone=args['phone'],
            mail=args['mail'],
            profile_image_link=args['profile_image_link'],
            public=args['public'],
            taggable=args['taggable'],
            state="PENDING"
        )

        try:
            user_persistent = user_service.register_user(user)
        except Exception as e:
            return (e.message if hasattr(e, 'message') else str(e),400)
            
        if user_persistent:
            dt = user_persistent.get_dict()
            del dt['password']
            return (dt,200) 
            
        return 'Creating user failed',400


class FollowResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def post(self):
        # To be implemented.
        pass

class MuteResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def get(self):
        # To be implemented.
        pass


class BlockResource(Resource):
    def __init__(self):
        # To be implemented.
        pass

    def post(self):
        # To be implemented.
        pass
