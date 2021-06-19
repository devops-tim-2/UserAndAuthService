from broker.produce import publish
from models.models import AgentRequest, User
from exceptions.exceptions import InvalidRoleException
from repository import user_repository, agent_request_repository
import bcrypt 

def register_user(user:User) -> User:
    # Server validates sent data
    if user.role == 'agent':
        # Password is encrypted using bcrypt algorithm
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # User is saved to database with state set to PENDING
        user.state = 'PENDING'
        persisted_user = user_repository.create(user)
        # New entity is created in AgentRequest table with u_id pointing to created user id
        agent_request = AgentRequest(u_id=persisted_user.id)
        persisted_agent_request = agent_request_repository.create(agent_request)


        dt = persisted_user.get_dict()
        del dt['password']
        dt['agent_request_id'] = persisted_agent_request.id
        # agent.request.created event is sent to RabbitMQ
        publish('agent.request.created', dt)
        # If and when administrator approves registration request (when agent.request.approved event is catched), user state is set to ACCEPTED and user.created event is fired
        # If administrator rejects registration request (agent.request.rejected is catched), user state is set to REJECTED and no events are fired
    elif user.role == 'user':
        # Password is encrypted using bcrypt algorithm
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # User is saved to database with state set to ACCEPTED
        user.state = 'PENDING'
        persisted_user = user_repository.create(user)
        dt = persisted_user.get_dict()
        del dt['password']
        # user.created event is sent to RabbitMQ
        publish('user.created', dt)
    else:
        raise InvalidRoleException()

    return persisted_user