from common.database import db_session
from models.models import Block

def get(source, destination):
    return Block.query.filter(Block.src == source, Block.dst == destination).first()

def exists(source, destination):
    return db_session.query(Block.query.filter(Block.src == source, Block.dst == destination).exists()).scalar()

def create(block):
    db_session.add(block)
    db_session.commit()
    return block

def delete(source, destination):
    block = Block.query.filter(Block.src == source, Block.dst == destination).first()
    db_session.delete(block)
    db_session.commit()

def delete_with_user(user_id):
    blocks_src = Block.query.filter(Block.src == user_id).delete()
    blocks_dst = Block.query.filter(Block.dst == user_id).delete()
    db_session.commit()

