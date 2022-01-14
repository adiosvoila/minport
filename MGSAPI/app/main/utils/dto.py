from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    add_user = api.model('add_user', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password'),
        'Authorization': fields.String(description='Optional auth token field')
    })
    
    del_user = api.model('del_user', {
        'username': fields.String(required=True, description='Username'),
        'Authorization': fields.String(description='Optional auth token field')
        })

class NodeDto:
    api = Namespace('node', description='get/set node data')
    update_node = api.model('update_node', {
        'node_name': fields.String(required=True, description='Node name'),
        'is_idpw_auth' : fields.Boolean(description='OVPN ID/PW Authentication Flag'),
        'ip_addr': fields.String(required=True, description='IPv4 Address'),
        'cert_key': fields.String(required=True, description='OVPN Profile(Base64)'),
        'Authorization': fields.String(description='Optional auth token field')
        })
    
    delete_node = api.model('delete_node', {
        'node_name': fields.String(required=True, description='Node name'),
        'Authorization': fields.String(description='Optional auth token field')}
    )

    reboot_node = api.model('reboot_node', {
        'node_name': fields.String(required=True, description='Node name'),
        'Authorization': fields.String(description='Optional auth token field')}
    )

    rename_node = api.model('rename_node', {
        'node_name': fields.String(required=True, description='Node name'),
        'new_node_name': fields.String(required=True, description='New node name'),
        'Authorization': fields.String(description='Optional auth token field')}
    )
    
    get_node = api.model('get_node', {
        'node_name': fields.String(description='Node name'),
        'is_idpw_auth' : fields.Boolean(description='OVPN ID/PW Authentication Flag'),
        'ip_addr': fields.String(description='IPv4 Address'),
#        'cert_key': fields.String(description='OVPN Profile(Base64)'),
        'updated_time': fields.DateTime(dt_format='iso8601')
#        'Authorization': fields.String(description='Optional auth token field')
        })

    get_node_cert_result = api.model('get_node_cert_result', {
        'node_name': fields.String(description='Node name'),
        'ip_addr': fields.String(description='IPv4 Address'),
        'updated_time': fields.DateTime(dt_format='iso8601'),
        'cert_key': fields.String(description='OVPN Profile(Base64)')
        })

    get_node_cert_expect = api.parser()
    get_node_cert_expect.add_argument('Authorization', type=str, location='headers', required=True,
                                      help='JWT authentication token')
    get_node_cert_expect.add_argument('node_name', type=str, location='args', required=True,
                                      help='Target node name')
    
    header = api.parser()
    header.add_argument('Authorization', type=str, location='headers', required=True,
                         help='JWT authentication token')

class AuthDto:
    api = Namespace('auth', description='JWT authentication operations')
    auth = api.model('auth', {
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password')
        })

class LeaseDto:
    api = Namespace('lease', description='SOCKS5 Server lease/release operations')
    lease = api.model('add_lease', {
        'node_name': fields.String(required=True, description='Target node name'),
        'username': fields.String(required=True, description='Client username'),
        'password': fields.String(required=True, description='Client password'),
        'period': fields.Integer(required=True, description='Lease period'),
        'Authorization': fields.String(description='Optional auth token field')
        })

    release = api.model('delete_lease', {
        'node_name': fields.String(required=True, description='Target node name'),
        'username': fields.String(required=True, description='Target username'),
        'Authorization': fields.String(description='Optional auth token field')
        })
    
    get_lease = api.model('get_lease', {
        'username': fields.String(description='Socks5 server username'),
        'password': fields.String(description='Socks5 server password'),
        'node_name': fields.String(description='Socks5 server node_name'),
        'expire_date': fields.DateTime(dt_format='iso8601'),
        })
    header = api.parser()
    header.add_argument('Authorization', type=str, location='headers', required=True,
                        help='JWT authentication token')


