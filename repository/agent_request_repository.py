from common.database import db_session

def create(agent_request):
    db_session.add(agent_request)
    db_session.commit()

    return agent_request