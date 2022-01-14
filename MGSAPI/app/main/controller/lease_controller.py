from flask import request
from flask_restplus import Resource

from ..utils.dto import LeaseDto
from ..service.lease_service import add_lease, delete_lease, get_all_leases 
from ..utils.decorator import token_required, admin_token_required

api = LeaseDto.api

@api.route('/')
class LeaseList(Resource):
    @token_required
    @api.doc('List of every lease information')
    @api.marshal_list_with(LeaseDto.get_lease, code=200)
    @api.expect(LeaseDto.header)
    def get(self):
        #Listing all lease information
        return get_all_leases()

    @admin_token_required
    @api.response(201, '{\n"status":"success", \n\
                        "message":"New lease added successfully."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Socks server user is duplicated."\n}')
    @api.response(500, '{\n"status": "fail",\n\
                        "message": "<SSH_Exception>"\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "Target node is not exist."\n}')

    @api.doc('Add SOCKS5 server lease.')
    @api.expect(LeaseDto.lease, validate=True)
    def post(self):
        #Add new lease
        data = request.json
        return add_lease(data=data)
    
    @token_required
    @api.response(200, '{\n"status":"success", \n\
                        "message":"Successfully Deleted."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required parameters."\n}')
    @api.response(500, '{\n"status": "fail",\n\
                        "message": "<SSH_Exception>"\n}')

    @api.doc('Delete a lease')
    @api.expect(LeaseDto.release, validate=True)
    def delete(self):
        #Delete lease
        data = request.json
        return delete_lease(data=data)
