from flask import request
from flask_restplus import Resource, marshal

from ..utils.decorator import token_required, admin_token_required
from ..utils.dto import NodeDto
from ..service.node_service import update_node_data, get_all_nodes, delete_node, change_mac_addr,\
                                   get_cert, reboot_node, rename_node, switchidpwauth_node

api = NodeDto.api

@api.route('/')
class NodeList(Resource):
    @token_required 
    @api.marshal_list_with(NodeDto.get_node)
    @api.response(200, '{\n"status": "success",\n\
                        "message": "[List of node information]"\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail"\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('List of every node information')
    @api.expect(NodeDto.header)
    def get(self):
        #Listing all node information
        return get_all_nodes()
    
    @token_required
    @api.response(201, '{\n"status": "success",\n\
                        "message": "New node added successfully."\n}')
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Node data is successfully updated."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail"\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('Add or Update node data')
    @api.expect(NodeDto.update_node, validate=True)
    def post(self):
        #Update node data
        data = request.json
        return update_node_data(data=data)

    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Successfully Deleted."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('Delete a node')
    @api.expect(NodeDto.delete_node, validate=True)
    def delete(self):
        #Delete node
        data = request.json
        return delete_node(data=data)

@api.route('/cert/')
class NodeCert(Resource):
    @token_required
    @api.response(200, model=NodeDto.get_node_cert_result, description='success')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')

#    @api.marshal_list_with(NodeDto.get_node_cert_result, code=200)
    @api.doc('Get single node OVPN Profile')
    @api.expect(NodeDto.get_node_cert_expect, validate=True)
    def get(self):
        #Get single node OVPN Profile
        node_name = request.args.get('node_name')
        message, code = get_cert(node_name=node_name)
        if code is 200:
            return marshal(message, NodeDto.get_node_cert_result), 200
        else:
            return message, code

@api.route('/mac/')
class MACAddr(Resource):
    @admin_token_required #unpriviliged user also approved?
    @api.response(200, '{\n"status":"success", \n\
                        "mac_addr":"<changed_MAC_Addr>", \n\
                        "message":"MAC Address is successfully updated."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.response(500, '{\n"status": "fail",\n\
                        "message": "<SSH_Exception>"\n}')
    @api.doc('Change node MAC Address')
    #Borrow from delete_node Dto
    @api.expect(NodeDto.delete_node, validate=True)
    def post(self):
        data = request.json
        return change_mac_addr(data=data)

@api.route('/reboot/')
class RebootNode(Resource):
    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Successfully Rebooted."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('Reboot a node')
    @api.expect(NodeDto.reboot_node, validate=True)
    def post(self):
        #Reboot node
        data = request.json
        return reboot_node(data=data)

@api.route('/rename/')
class RenameNode(Resource):
    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Successfully Changed."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('Rename a node')
    @api.expect(NodeDto.rename_node, validate=True)
    def put(self):
        #Rename node
        data = request.json
        return rename_node(data=data)

@api.route('/switchidpwauth/')
class SwitchIDPWAuth(Resource):
    @admin_token_required
    @api.response(200, '{\n"status": "success",\n\
                        "message": "Successfully Changed."\n}')
    @api.response(404, '{\n"status": "fail",\n\
                        "message": "A node is not exist."\n}')
    @api.response(401, '{\n"status": "fail",\n\
                        "message": "No auth key",\n}\n\
                        {\n"status": "fail",\n\
                        "message": "Authentication Fail Reason"\n}')
    @api.response(400, '{\n"status": "fail",\n\
                        "message": "Request message does not contains required paramaters."\n}')
    @api.doc('ON/OFF ID/PW Auth for node')
    @api.expect(NodeDto.reboot_node, validate=True) #Borrow from reboot_node
    def put(self):
        data = request.json
        return switchidpwauth_node(data=data)
