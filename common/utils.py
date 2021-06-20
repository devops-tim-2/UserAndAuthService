from os import environ
from datetime import datetime
import jwt
from exceptions.exceptions import NotAuthorizedException, TokenExpiredException

def auth(headers):
    if not ('Authorization' in headers):
        raise NotAuthorizedException()

    token = headers['Authorization'].split(' ')[1]
    try:
        payload = jwt.decode(token, environ.get('JWT_SECRET'), environ.get('JWT_ALGORITHM'))
    except Exception:
        raise NotAuthorizedException()

    exp = payload['exp']
    if datetime.now() > datetime.fromtimestamp(exp / 1000.0):
        raise TokenExpiredException()

    return payload
