from .. import db
from . import node

class Lease(db.Model):
    """SOCKS5 Sever Lease model which storing usrname, """
    __tablename__ = "MGS_LEASE"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    node_name = db.Column(db.String(100), db.ForeignKey('MGS_NODE.node_name', onupdate="cascade"))
    expire_date = db.Column(db.DateTime)

 #   node = db.relationship("Node", backref=db.backref('node_name'))
