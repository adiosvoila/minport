import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    try:
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            new_user = User(
                    username=data['username'],
                    password=data['password'],
                    admin=True
                    )
            save_changes(new_user)
            response_object = {
                'status': 'success',
                'message': 'Successfully Registered.'
            }
            return response_object, 201

        else:
            response_object = {
                'status':'fail',
                'message':'Username is duplicated!'
            }
            return response_object, 403
    
    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters.'
        }
        return response_object, 400
    

def delete_user(data):
    try:
        user = User.query.filter_by(username=data['username']).first()
        if user:
            db.session.delete(user)
            # Commit query
            db.session.commit()
            response_object = {
                'status':'success',
                'message': 'Successfully Deleted.'
            }
            return response_object, 200
        
        else:
            response_object = {
                'status': 'fail',
                'message': 'User is not exist.'
            }
            return response_object, 404
    
    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters.'
        }
        return response_object, 400

def modify_user(data):
    try:
        user = User.query.filter_by(username=data['username']).first()
        if user:
            password=data['password']
            user.password=password
            db.session.commit()
            
            response_object = {
                'status':'success',
                'message': 'Successfully Updated.'
            }
            return response_object, 200
        
        else:
            response_object = {
                'status': 'fail',
                'message': 'User is not exist.'
            }
            return response_object, 404
    
    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters.'
        }
        return response_object, 400



def save_changes(data):
    db.session.add(data)
    db.session.commit()
