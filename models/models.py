from common.database import db
import dataclasses

@dataclasses.dataclass
class User(db.Model):
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(127),unique=True, nullable=False)
    password = db.Column(db.String(127), nullable=False)
    role = db.Column(db.String(127), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(127), nullable=False)
    region = db.Column(db.String(127), nullable=False)
    interests = db.Column(db.String(127), nullable=False)
    bio = db.Column(db.String(127), nullable=False)
    website = db.Column(db.String(127), nullable=False)
    phone = db.Column(db.String(127), nullable=False)
    mail = db.Column(db.String(127),unique=True, nullable=False)
    profile_image_link = db.Column(db.String(127), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    taggable = db.Column(db.Boolean, nullable=False)
    state = db.Column(db.String(127), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def get_dict(self):
        return dataclasses.asdict(self)
        

@dataclasses.dataclass
class Follow(db.Model):
    id: int
    src: int
    dst: int
    mute: bool

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mute = db.Column(db.Boolean, nullable=False)
    src = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dst = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Follow {self.src}->{self.dst} ({self.mute})>'

    def get_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Block(db.Model):
    id: int
    src: int
    dst: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    src = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dst = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Block {self.src}->{self.dst}>'

    def get_dict(self):
        return dataclasses.asdict(self)



@dataclasses.dataclass
class AgentRequest(db.Model):
    id: int
    u_id: int

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<AgentRequest {self.u_id}>'

    def get_dict(self):
        return dataclasses.asdict(self)

