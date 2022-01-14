from flask import request
from flask_restplus import Resource

from app.main.service.auth_service import Auth
from ..utils.dto import AuthDto

api = AuthDto.api

@api.route('/')
class UserLogin(Resource):
    @api.response(200, '{\n"status":"success",\n\
                 "message":"Successfully logged in."\n}')
    @api.response(400, '{\n"status":"fail",\n\
                 "messasge": "Request message does not contains required paramaters."\n}')
    @api.response(401, '{\n"status":"fail",\n\
                 "messasge": "Username or Password does not match."\n}')
    @api.doc('User Login')
    @api.expect(AuthDto.auth, validate=True)
    def post(self):
        data = request.json
        return Auth.login_user(data=data)
