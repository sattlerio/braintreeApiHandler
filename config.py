import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    BUILD_NUMBER = "##BUILD_NUMBER##"
    BUILD_ID = "##BUILD_ID##"
    BUILD_TAG = "##BUILD_TAG##"
    GIT_COMMIT = "##GIT_COMMIT##"

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True