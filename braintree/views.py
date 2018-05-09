from flask import jsonify, request, Blueprint, Response, current_app as app

braintree = Blueprint('braintree', __name__)


@braintree.route('/ping', methods=['GET'])
def test():
    return "pong"
