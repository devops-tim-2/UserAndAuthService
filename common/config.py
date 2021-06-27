from controller.user_controller import CocreteFollowResource
from models.models import FollowRequest
from os import environ
from flask_cors import CORS
from flask.app import Flask
from flask_wtf import CSRFProtect
from flask_restful import Api

config = {
    'test': 'TEST_DATABASE_URI',
    'dev': 'DEV_DATABASE_URI'
}

def setup_config(cfg_name: str):
    environ['SQLALCHEMY_DATABASE_URI'] = environ.get(config[cfg_name])
    
    app = Flask(__name__)
    
    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)
        
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "send_wildcard": "False"}}) 
    api = Api(app)


    # This import must be postponed because importing common.database has side-effects
    from common.database import init_db
    init_db()


    # This import must be postponed after init_db has been called
    from controller.user_controller import UserResource, UserListResource, LoginResource, RegisterResource, FollowResource, MuteResource, BlockResource
    api.add_resource(UserResource, '/api/<user_id>')
    api.add_resource(UserListResource, '/api')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(FollowResource, '/api/follow')
    api.add_resource(CocreteFollowResource, '/api/concretefollow/<dst>')
    api.add_resource(MuteResource, '/api/follow/mute')
    api.add_resource(BlockResource, '/api/block')


    # This import must be postponed after init_db has been called
    from models.models import AgentRequest, User, Follow, Block
    if cfg_name == 'test':
        User.query.delete()
        Follow.query.delete()
        Block.query.delete()
        AgentRequest.query.delete()
        FollowRequest.query.delete()
    
    return app
