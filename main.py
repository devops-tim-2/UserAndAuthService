from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)
api = Api(app)

from controller.user_controller import UserResource, UserListResource, LoginResource, RegisterResource, FollowResource, MuteResource, BlockResource
api.add_resource(UserResource, '/api/<user_id>')
api.add_resource(UserListResource, '/api')
api.add_resource(LoginResource, '/api/login')
api.add_resource(RegisterResource, '/api/register')
api.add_resource(FollowResource, '/api/follow')
api.add_resource(MuteResource, '/api/follow/mute')
api.add_resource(BlockResource, '/api/block')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

