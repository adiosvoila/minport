from functools import wraps
from flask import request

from app.main.service.auth_service import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        username = data.get('username')

        if not username:
            return data, status
        #else
        return f(*args, **kwargs)

    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        username = data.get('username')

        if not username:
            return data, status

        admin = data.get('admin')
        
        if not admin: #False
            response_object = {
                'status': 'fail',
                'message': 'Admin token is required.'
            }
            return response_object, 401
        #True
        return f(*args, **kwargs)

    return decorated
