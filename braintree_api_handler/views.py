from flask import jsonify, request, Blueprint, Response, current_app as app
import uuid
import braintree

braintree_handler = Blueprint('braintree_handler', __name__)


@braintree_handler.route('/ping', methods=['GET'])
def test():
    return "pong"


@braintree_handler.route("/validate-credentials", methods=['POST'])
def validate_credentials():
    transaction_id = request.headers.get("x-transactionid", "")
    if not transaction_id:
        app.logger.info("no transaction id header present")
        transaction_id = str(uuid.uuid4())

    app.logger.info("{}: got new transaction to validate braintree credentials".format(transaction_id))

    if not request.is_json or not request.data:
        app.logger.info("{}: no valid json submitted abort transaction".format(transaction_id))
        return jsonify({"status": "ERROR",
                        "status_code": 400,
                        "message": "please submit a valid json body",
                        "transaction_id": transaction_id}), 400

    if not "merchant_id" in data or not "environment" in data or not "public_key" in data or not "private_key" in data:
        app.logger.info("{}: the post request has missing fields".format(transaction_id))
        return jsonify({"status": "ERROR",
                        "status_code": 400,
                        "message": "you have to submit merchant_id, environment, public_key and private key",
                        "transaction_id": transaction_id}), 400

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id="use_your_merchant_id",
            public_key="use_your_public_key",
            private_key="use_your_private_key"
        )
    )

    client_token = gateway.client_token.generate({
        "customer_id": "demo"
    })

    return "d"
