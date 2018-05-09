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

    data = request.get_json()

    if not "merchant_id" in data or not "environment" in data or not "public_key" in data or not "private_key" in data:
        app.logger.info("{}: the post request has missing fields".format(transaction_id))
        return jsonify({"status": "ERROR",
                        "status_code": 400,
                        "message": "you have to submit merchant_id, environment, public_key and private key",
                        "transaction_id": transaction_id}), 400

    if data["environment"] not in ["production", "sandbox"]:
        app.logger.info("{}: no valid environment submitted, going to abort transaction".format(transaction_id))
        return jsonify(
            status="ERROR",
            status_code=400,
            message="environment must be either production or sandbox",
            transaction_id=transaction_id
        )

    try:
        if data["environment"] == 'production':
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=environment,
                merchant_id=data["merchant_id"],
                public_key=data["public_key"],
                private_key=data["private_key"]
            )
        )

        try:
            client_token = gateway.client_token.generate({})

            app.logger.info("{}: successfully validated credentials: {}".format(transaction_id, client_token))
            return jsonify(status="INFO",
                           status_code=200,
                           message="successfully validated credentials",
                           token=client_token,
                           transaction_id=transaction_id)
        except Exception as e:
            app.logger.info(e)
            app.logger.info("{}: error while trying to retrieve token".format(transaction_id))
            return jsonify(status="ERROR",
                           status_code=401,
                           message="not possible to authenticate user",
                           transaction_id=transaction_id), 401
    except Exception as e:
        app.logger.info(e)
        app.logger.info("{}: error while trying to generate token".format(transaction_id))
        return jsonify(status="ERROR",
                       status_code=500,
                       message="not possible to authenticate user",
                       transaction_id=transaction_id), 500

    return "d"
