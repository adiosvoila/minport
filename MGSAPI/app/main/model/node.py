from .. import db
from . import lease

class Node(db.Model):
    #Node model for storing Node name, IP, Cert_Key, Last Updated time
    __tablename__ = "MGS_NODE"

    node_name = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    ip_addr = db.Column(db.String(50))
    cert_key = db.Column(db.Text)
    updated_time = db.Column(db.DateTime)
    is_idpw_auth = db.Column(db.Boolean, nullable=False, default=True) # ID/PW Auth Indicator

    lease = db.relationship("Lease")
