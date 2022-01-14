from .. import db, flask_bcrypt
from ..config import key
import datetime
import jwt

class User(db.Model):
    """User Model for storing user related details"""
    __tablename__ = "MGS_USER"

    username = db.Column(db.String(50), primary_key=True, unique=True)
    password_hash = db.Column(db.String(100))
    admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)
    
    def encode_auth_token(self, username):
        try:
            payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                    'iat': datetime.datetime.utcnow(),
                    'sub': username
            }
            return jwt.encode(
                    payload,
                    key,
                    algorithm='HS256'
            )
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key)
            return {'username':payload['sub']}
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log-in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log-in again.'
        except jwt.DecodeError:
            return 'Decode failed. Invalid token was offered.'
        except Exception as e:
            return str(e)

    def __repr__(self):
        return "<user '{}'>".format(self.username)
