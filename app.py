import os
import random
import requests
import sys
from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain, ChainReplacementError
from wallet.wallet import Wallet
from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool

from pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route("/")
@app.route("/blockchain")
def get_blockchain():
    return jsonify(blockchain.serialize())


@app.route("/blockchain/mine")
def mine():
    transaction_data = "somedata"
    blockchain.add_block(transaction_data)

    block = blockchain.last_block

    pubsub.broadcast_block(block)

    return jsonify(block.serialize())


@app.route("/wallet/transaction", methods=["POST"])
def transaction():
    data = request.get_json()

    transaction = transaction_pool.has_existing_transaction(wallet.address)

    if transaction:
        transaction.update(wallet, data["recipient_address"], data["amount"])
    else:
        transaction = Transaction(wallet, data["recipient_address"], data["amount"])

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.serialize())


ROOT_PORT = 5000
PORT = ROOT_PORT

# For convenience, it is easier to pass the 'peer' option when running the file from the command line. This may need to change in future.
if (
    os.environ.get("PEER") == "1"
    or os.environ.get("PEER") == "True"
    or "peer" in sys.argv
):
    PORT = random.randint(5001, 6000)

    result = requests.get("http://localhost:{}/blockchain".format(ROOT_PORT))
    result_blockchain = Blockchain.deserialize(result.json())

    try:
        blockchain.replace(result_blockchain.chain)
        print("Successfully synchronized the node.")
    except ChainReplacementError as e:
        print("Error synchronizing the node - {}".format(e.message))

app.run(port=PORT)

if __name__ == "__main__":
    pass
