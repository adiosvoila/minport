from app.main.model.user import User
import sys


class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(username=data['username']).first()
            if user and user.check_password(data['password']):
                auth_token = user.encode_auth_token(username=data['username'])
                if auth_token:
                    response_object = {
                        'status':'success',
                        'message':'Successfully logged in.',
                        'Authorization': auth_token.decode('UTF-8')
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status':'fail',
                    'message': 'Username or Password does not match.'
                }
                return response_object, 401

        except (KeyError, TypeError) as e:
            response_object = {
                'status': 'fail',
                'message': 'Request message does not contains required paramaters.'
            }
            return response_object, 400
    
    @staticmethod
    def get_logged_in_user(data):
        #First, get auth token from header
        #Then next, get token from payload
        try:
            auth_token = data.headers.get('Authorization')
        except Exception as e:
            pass 
        #Maybe payload can contains token
        #If payload also doesn't have token, return 401.
        if not auth_token:
            try:
                auth_token = data.json['Authorization']
            except (KeyError,TypeError) as e:
                response_object = {
                    'status': 'fail',
                    'message': 'No auth token.'
                }
                return response_object, 401
        
        #DEBUG print(auth_token, file=sys.stderr)
        #Check None
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                #Extract username from dictionary
                username=resp['username']
                user = User.query.filter_by(username=username).first()
                
                #For internal validation(admin/user)
                response_object = {
                    'status': 'success',
                    'username': user.username,
                    'admin': user.admin
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'No auth token.'
            }
        return response_object, 401

