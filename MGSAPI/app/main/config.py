import os

# uncomment the line below for postgres database url from env variable
postgres_local_base = "postgresql://localhost/mgs_api_prod"

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SETCRET_KEY', 'xH.pjnZn?u6cqz1YnnnM')
    SSH_KEY = 'nd5YmCfb-5Lh>DcGIThY'
    SSH_PORT = 2220
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    #SQLALCHEMY_DATABASE_URI = postgre_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_prod.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
ssh_key = Config.SSH_KEY
ssh_port = Config.SSH_PORT
