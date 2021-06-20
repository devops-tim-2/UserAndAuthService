from dataclasses import dataclass, asdict

from sqlalchemy import Column, Integer, String, Boolean, \
     ForeignKey

from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base(name='Model')


USER_ID_FIELD = 'user.id'
FOLLOW_ID_FIELD = 'follow.id'

@dataclass
class User(Model):
    __tablename__ = 'user'
    id: int
    username: str
    password: str
    role: str
    age: int
    sex: str
    region: str
    interests: str
    bio: str
    website: str
    phone: str
    mail: str
    profile_image_link: str
    public: bool
    taggable: bool
    state: str #PENDING, ACCEPTED, REJECTED

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(127),unique=True, nullable=False)
    password = Column(String(127), nullable=False)
    role = Column(String(127), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(127), nullable=False)
    region = Column(String(127), nullable=False)
    interests = Column(String(127), nullable=False)
    bio = Column(String(127), nullable=False)
    website = Column(String(127), nullable=False)
    phone = Column(String(127), nullable=False)
    mail = Column(String(127),unique=True, nullable=False)
    profile_image_link = Column(String(127), nullable=False)
    public = Column(Boolean, nullable=False)
    taggable = Column(Boolean, nullable=False)
    state = Column(String(127), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def get_dict(self):
        return asdict(self)
        

@dataclass
class Follow(Model):
    __tablename__ = 'follow'
    id: int
    src: int
    dst: int
    mute: bool

    id = Column(Integer, primary_key=True, autoincrement=True)
    mute = Column(Boolean, nullable=False)
    src = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    dst = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    
    def __repr__(self):
        return f'<Follow {self.src}->{self.dst} ({self.mute})>'

    def get_dict(self):
        return asdict(self)

@dataclass
class FollowRequest(Model):
    __tablename__ = 'followrequest'
    id: int
    src: int
    dst: int
    mute: bool

    id = Column(Integer, primary_key=True, autoincrement=True)
    mute = Column(Boolean, nullable=False)
    src = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    dst = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    
    def __repr__(self):
        return f'<FollowRequest {self.src}->{self.dst} ({self.mute})>'

    def get_dict(self):
        return asdict(self)

@dataclass
class Block(Model):
    __tablename__ = 'block'
    id: int
    src: int
    dst: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    dst = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    
    def __repr__(self):
        return f'<Block {self.src}->{self.dst}>'

    def get_dict(self):
        return asdict(self)



@dataclass
class AgentRequest(Model):
    __tablename__ = 'agentrequest'
    id: int
    u_id: int

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer, ForeignKey(USER_ID_FIELD), nullable=False)
    
    def __repr__(self):
        return f'<AgentRequest {self.u_id}>'

    def get_dict(self):
        return asdict(self)

