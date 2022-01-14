import uuid
import datetime,sys

from app.main import db
from app.main.model.lease import Lease
#for ip_addr
from app.main.model.node import Node
#for VM SSH Login
from ..config import ssh_key, ssh_port

from ..utils.ssh import SshClient
#Macros
CMD_CREATE_USER = 'useradd -M -N '
CMD_DELETE_USER = 'deluser '
CMD_CHANGE_PASSWORD1 = 'echo -e "'
CMD_CHANGE_PASSWORD2 = '" | passwd '

def add_lease(data):
    try:
        #Check Node is exist
        node = Node.query.filter_by(node_name=data['node_name']).first()
        if not node:
            response_object = {
                'status':'fail',
                'message':'Target node is not exist.'
            }
            return response_object, 404

        lease = Lease.query.filter_by(node_name=data['node_name'], username=data['username']).first()
        if not lease:            
            _ip_addr = Node.query.filter_by(node_name=data['node_name']).first().ip_addr
            socks_username = data['username']
            socks_password = data['password']
            socks_period = data['period']
            #TODO: Sanity check
            if None in [socks_username, socks_password, socks_period]:
                raise KeyError('Wrong parameters')
            #SSH_Exceptions
            try:
                client = SshClient()
                client.connect(ip_addr=_ip_addr, username='root', password=ssh_key, port=ssh_port)
                #Create new user
                cmd = CMD_CREATE_USER + socks_username
                client.exec_cmd(cmd)

                #Change Password
                cmd = CMD_CHANGE_PASSWORD1 + socks_password + '\n' + socks_password + '\n' +\
                      CMD_CHANGE_PASSWORD2 + socks_username
                client.exec_cmd(cmd)
                client.disconnect()
            except Exception as e:
                response_object = {
                        'status': 'fail',
                        'message': str(e)
                }
                return response_object, 500

            new_lease = Lease(
                username=data['username'],
                password=data['password'],
                node_name=data['node_name'],
                # We're using KST!
                expire_date=datetime.datetime.now() + datetime.timedelta(days=socks_period)
            )
            #Add new column
            db.session.add(new_lease)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'New lease added successfully.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Socks server user is duplicated.'
            }
            return response_object, 400

    except (KeyError, TypeError) as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters.'
        }
        return response_object, 400


def get_all_leases():

    return Lease.query.order_by(Lease.node_name.asc()).all()


def delete_lease(data):
    try:
        lease = Lease.query.filter_by(node_name=data['node_name'], username=data['username']).first()
        if not lease:
            response_object = {
                'status': 'fail',
                'message': 'Lease in condition is not exist.'
            }
            return response_object, 404
        else:
            _ip_addr = Node.query.filter_by(node_name=data['node_name']).first().ip_addr
            socks_username = data['username']
            #SSH Exceptions
            try:
                #Connect to target server
                client = SshClient()
                client.connect(ip_addr=_ip_addr, username='root', password=ssh_key, port=ssh_port)
                #Delete user
                cmd = CMD_DELETE_USER + socks_username
                client.exec_cmd(cmd)
                client.disconnect()
            except Exception as e:
                response_object = {
                        'status': 'fail',
                        'message': str(e)
                }
                return response_object, 500
            db.session.delete(lease)
            #Commit changes
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully Deleted.'
            }
            return response_object, 200

    except (KeyError, TypeError) as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters.'
        }
        return response_object, 400

