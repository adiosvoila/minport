import uuid
import datetime
import random, sys

from app.main import db
from app.main.model.node import Node
from app.main.model.lease import Lease
#for VM SSH Login
from ..config import ssh_key, ssh_port
from ..utils.ssh import SshClient

#Macros
MAC_OUI_STR = '00:50:56'
CMD_CHANGE_MAC1 = 'uci set network.wan.macaddr='
CMD_CHANGE_MAC2 = 'uci commit network'
CMD_REBOOT = 'reboot'
UUID_PATH = '/etc/uuid'
CMD_ENABLE_IDPW_AUTH1 = 'cat /usr/enable_idpw_update_node > /etc/init.d/update_node'
CMD_ENABLE_IDPW_AUTH2 = 'cat /usr/enable_idpw_server.conf > /etc/openvpn/server.conf'
CMD_DISABLE_IDPW_AUTH1 = 'cat /usr/disable_idpw_update_node > /etc/init.d/update_node'
CMD_DISABLE_IDPW_AUTH2 = 'cat /usr/disable_idpw_server.conf > /etc/openvpn/server.conf'

def update_node_data(data):
    try:
        node = Node.query.filter_by(node_name=data['node_name']).first()
        if not node:
            new_node = Node(
                node_name=data['node_name'],
                ip_addr=data['ip_addr'],
                cert_key=data['cert_key'],
                # We're using KST!
                updated_time=datetime.datetime.now()
            )
            #Add new column
            db.session.add(new_node)
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'New node added successfully.'
            }
            return response_object, 201
        else:
            node.ip_addr=data['ip_addr']
            node.cert_key=data['cert_key']
            node.updated_time=datetime.datetime.now()
            #Commit changes
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Node data is successfully updated.'
            }
            return response_object, 200

    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters'
        }
        return response_object, 400


def get_all_nodes():
    return Node.query.order_by(Node.node_name.asc()).all()


def delete_node(data):
    try:
        node = Node.query.filter_by(node_name=data['node_name']).first()
        if not node:
            response_object = {
                'status': 'fail',
                'message': 'A node is not exist.'
            }
            return response_object, 404
        else:
            db.session.delete(node)
            #Commit changes
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully Deleted.'
            }
            return response_object, 200

    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters'
        }
        return response_object, 400

def change_mac_addr(data):
    try:
        node = Node.query.filter_by(node_name=data['node_name']).first()
        if not node:
            response_object = {
                'status': 'fail',
                'message': 'A node is not exist.'
            }
            return response_object, 404
        else:
            #Generate MAC(TODO: Avoid MAC Collision, but almost impossble)
            byte_fmt='%02x'
            prefix = [int(chunk, 16) for chunk in MAC_OUI_STR.split(':')]
            #VMware Prefix is valid between 0x00 and 0x3F
            prefix = prefix + [random.randrange(63)]
            mac = prefix + [random.randrange(256) for _ in range(2)]
            mac_addr = ':'.join(byte_fmt % b for b in mac)
            #TODO:IP sanity check
            #SSH Exceptions
            try:
                client = SshClient()
                client.connect(ip_addr=node.ip_addr, username='root', password=ssh_key, port=ssh_port)
                #Change MAC Address
                cmd = CMD_CHANGE_MAC1 + mac_addr
                client.exec_cmd(cmd)
                cmd = CMD_CHANGE_MAC2
                client.exec_cmd(cmd)
                #Reboot
                cmd = CMD_REBOOT
                client.exec_cmd(cmd)
                client.disconnect()
            except Exception as e:
                response_object = {
                        'status': 'fail',
                        'message': str(e)
                }
                return response_object, 500

    except KeyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Request message does not contains required paramaters'
        }
        return response_object, 400

    response_object = {
        'status': 'success',
        'mac_addr': mac_addr,
        'message': 'MAC Address is successfully updated.'
     }

    return response_object, 200

def get_cert(node_name):
#Get single node ovpn profile    
    try:
        node = Node.query.filter_by(node_name=node_name).first()
        if not node:
            response_object = {
                'status': 'fail',
                'message': 'A node is not exist.'
            }
            return response_object, 404
        #If node is exist
        else:
            #Because get_cert function doesn't use marshal_with decorator
            #We SHOULD return http response code.
            return node, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return response_object, 500

def reboot_node(data):
    node = Node.query.filter_by(node_name=data['node_name']).first()
    if not node:
        response_object = {
            'status': 'fail',
            'message': 'A node is not exist.'
        }
        return response_object, 404
    else:
        try:
            client = SshClient()
            client.connect(ip_addr=node.ip_addr, username='root', password=ssh_key, port=ssh_port)
            client.exec_cmd(CMD_REBOOT)
            client.disconnect()
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }  
            return response_object, 500

    response_object = {
        'status': 'success',
        'message': 'Successfully Rebooted.'
    }
    return response_object, 200

def rename_node(data):
    node = Node.query.filter_by(node_name=data['node_name']).first()
    if not node:
        response_object = {
            'status': 'fail',
            'message': 'A node is not exist.'
        }
        return response_object, 404
    else:
        try:
            client = SshClient()
            client.connect(ip_addr=node.ip_addr, username='root', password=ssh_key, port=ssh_port)
            cmd = 'echo ' + data['new_node_name'] + ' > ' + UUID_PATH
            client.exec_cmd(cmd)
            client.disconnect()
            # Update Node Record
            node.node_name = data['new_node_name']
            db.session.commit()

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }  
            return response_object, 500

    # Update lease record
    lease_list = Lease.query.filter_by(node_name=data['node_name'])
    for item in lease_list:
        item.node_name = data['new_node_name']
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Successfully Changed.'
    }
    return response_object, 200

def switchidpwauth_node(data):
    node = Node.query.filter_by(node_name=data['node_name']).first()
    if not node:
        response_object = {
            'status': 'fail',
            'message': 'A node is not exist.'
        }
        return response_object, 404
    else:
        try:
            client = SshClient()
            client.connect(ip_addr=node.ip_addr, username='root', password=ssh_key, port=ssh_port)
            if node.is_idpw_auth: #True
                client.exec_cmd(CMD_DISABLE_IDPW_AUTH1)
                client.exec_cmd(CMD_DISABLE_IDPW_AUTH2)
                node.is_idpw_auth = False
            else:
                client.exec_cmd(CMD_ENABLE_IDPW_AUTH1)
                client.exec_cmd(CMD_ENABLE_IDPW_AUTH2)
                node.is_idpw_auth = True
            # Commit changes
            db.session.commit()
            # Reboot Node               
            client.exec_cmd(CMD_REBOOT)
            client.disconnect()
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }  
            return response_object, 500

    response_object = {
        'status': 'success',
        'message': 'Successfully Rebooted.'
    }
    return response_object, 200
 
