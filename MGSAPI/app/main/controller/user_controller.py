from flask import request
from flask_restplus import Resource

from ..utils.dto import UserDto
from ..service.user_service import save_new_user, delete_user, modify_user
from ..utils.decorator import token_required, admin_token_required

api = UserDto.api

@api.route('/')
class AddUser(Resource):
    @admin_token_required
    @api.response(201, '{\n"status": "success",\n\
                       "message": "Successfully Registered."\n}')
    @api.response(403, '{\n"status": "fail",\n\
                       "message": "Username is duplicated!"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                       "message": "Request message does not contains required paramaters."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                       "message": "Authentication Fail Reason"\n}')



    @api.doc('Create a user')
    @api.expect(UserDto.add_user, validate=True)
    def post(self):
        #Creates new User
        data = request.json
        return save_new_user(data=data)

    #Delete User
    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Successfully Deleted."\n}')
    @api.response(403, '{\n"status": "fail",\n\
                        "message": "User is not exist."\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')

    @api.doc('Delete user')
    @api.expect(UserDto.del_user, validate=True)
    def delete(self):
        #Delete user
        data = request.json
        return delete_user(data=data)

    #Modify User
    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                       "message": "Successfully Updated."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                       "message": "User is not exist."\n}')
    @api.response(400, '{\n"status": "fail",\n\
                       "message": "Request message does not contains required paramaters."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                       "message": "Authentication Fail Reason"\n}')



    @api.doc('Update user password')
    @api.expect(UserDto.add_user, validate=True)
    def put(self):
        #Update User Password
        data = request.json
        return modify_user(data=data)
