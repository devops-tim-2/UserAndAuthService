from models.models import AgentRequest, User, Follow, Block
from os import environ
from typing import Tuple
from flask_cors import CORS
from flask_restful import Api
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from common.database import db
from flask_wtf import CSRFProtect


DevConfig = {
    'DEBUG': True,
    'DEVELOPMENT': True,
    'SQLALCHEMY_DATABASE_URI': f'{environ.get("DB_TYPE")}+{environ.get("DB_DRIVER")}://{environ.get("DB_USER")}:{environ.get("DB_PASSWORD")}@{environ.get("DB_HOST")}/{environ.get("DB_NAME")}',
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}


ProdConfig = {}


TestConfig = {
    'DEBUG': False,
    'DEVELOPMENT': True,
    'SQLALCHEMY_DATABASE_URI': f'{environ.get("TEST_DATABASE_URI")}',
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}


config: dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}


def setup_config(cfg_name: str) -> Tuple[Flask, SQLAlchemy]:
    app = Flask(__name__)
    
    if environ.get('ENABLE_CSRF') == 1:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['WTF_CSRF_SECRET_KEY'] = environ.get('WTF_CSRF_SECRET_KEY')
        csrf = CSRFProtect()
        csrf.init_app(app)
        
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "send_wildcard": "False"}}) 
    api = Api(app)

    from controller.user_controller import UserResource, UserListResource, LoginResource, RegisterResource, FollowResource, MuteResource, BlockResource
    api.add_resource(UserResource, '/api/<user_id>')
    api.add_resource(UserListResource, '/api')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(FollowResource, '/api/follow')
    api.add_resource(MuteResource, '/api/follow/mute')
    api.add_resource(BlockResource, '/api/block')

    cfg = config.get(cfg_name)
    for key in cfg.keys():
        app.config[key] = cfg[key]

    app.app_context().push()
    db.init_app(app)


    with app.app_context():
        db.create_all()

    if cfg_name == 'test':
        User.query.delete()
        Follow.query.delete()
        Block.query.delete()
        AgentRequest.query.delete()
    
    return app, db
