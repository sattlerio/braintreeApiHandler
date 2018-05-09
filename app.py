#!/usr/bin/env python

import sys
import logging

import unittest
from flask import Flask
from config import *

from braintree_api_handler.exceptions.configurations_exceptions import ImproperlyConfigured

ENVS = ['config.DevelopmentConfig', 'config.TestingConfig', 'config.StagingConfig', 'config.ProductionConfig']


def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


try:
    env_aux = get_env_variable("ENV").lower()
    ENV = env_aux if env_aux in ENVS else 'config.DevelopmentConfig'
except ImproperlyConfigured:
    ENV = 'config.DevelopmentConfig'

app = Flask(__name__)
app.config['ENV'] = ENV
app.config.from_object(ENV)

# app config
if ENV == ENVS[0]:
    # local development
    print("*** you should not see this message in production ***")

# log handler
log_level = logging.INFO if not app.config.get('DEBUG') else logging.DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

for h in app.logger.handlers:
    app.logger.removeHandler(h)
app.logger.addHandler(handler)
app.logger.setLevel(log_level)

# import blueprints
from braintree_api_handler.views import braintree_handler

# register blueprints
app.register_blueprint(braintree_handler)


@app.cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('app/tests', pattern='*_tests.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    app.run(debug=True)
