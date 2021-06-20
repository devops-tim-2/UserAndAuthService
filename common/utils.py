from os import environ
from datetime import datetime
import jwt

def auth(headers):
    if not ('Authorization' in headers):
        return 'Forbidden, unauthorized atempt.', 403

    token = headers['Authorization'].split(' ')[1]
    try:
        payload = jwt.decode(token, environ.get('JWT_SECRET'), environ.get('JWT_ALGORITHM'))
    except Exception:
        return 'Forbidden, invalid authentication.', 401

    exp = payload['exp']
    if datetime.now() > datetime.fromtimestamp(exp / 1000.0):
        return 'Forbidden, authorization token has expired.', 401

    return payload
