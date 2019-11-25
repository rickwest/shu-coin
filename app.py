import os
import random
import requests
import sys
from flask import Flask, jsonify, request
from blockchain.blockchain import Blockchain, ChainReplacementError
from wallet.wallet import Wallet
from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool
from flask_cors import CORS


from pubsub import PubSub

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# In future when app starts could broadcast a message saying node joined, then get a list of peers

blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route("/")
@app.route("/blockchain")
def get_blockchain():
    start = request.args.get("s")
    end = request.args.get("e")

    result = blockchain.serialize()[::-1]

    if start and end:
        return jsonify(result[int(start) : int(end)])

    return jsonify(result)


@app.route("/blockchain/mine")
def mine():
    # When a block is mined, add the serialized transactions from the transaction pool as it's data.
    transaction_data = transaction_pool.get_serialized_transactions()
    transaction_data.append(Transaction.reward(wallet).serialize())

    blockchain.add_block(transaction_data)

    block = blockchain.previous_block

    pubsub.broadcast_block(block)

    transaction_pool.clear_transactions(blockchain)

    return jsonify(block.serialize())


@app.route("/blockchain/length")
def length():
    return jsonify(len(blockchain.chain))


@app.route("/wallet/show")
def get_wallet():
    return jsonify({"address": wallet.address, "balance": wallet.balance})


@app.route("/wallet/transaction", methods=["POST"])
def transaction():
    data = request.get_json()

    # Check to see if a transaction already exists in the pool for this nodes wallet.
    # If it does, no need to create a new transaction, just update the existing one.
    # This will also be broadcast to all nodes and replace the exiting transaction.
    transaction = transaction_pool.get_transaction_for_address(wallet.address)

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
        # Synchronize with the blockchain
        blockchain.replace(result_blockchain.chain)
        print("Successfully synchronized the node.")
    except ChainReplacementError as e:
        print("Error synchronizing the node - {}".format(e.message))

if (
    os.environ.get("SEED") == "1"
    or os.environ.get("SEED") == "True"
    or "seed" in sys.argv
):
    for i in range(10):
        blockchain.add_block(
            [
                Transaction(
                    Wallet(), Wallet().address, random.randint(2, 50)
                ).serialize(),
                Transaction(
                    Wallet(), Wallet().address, random.randint(2, 50)
                ).serialize(),
            ]
        )
app.run(port=PORT)

if __name__ == "__main__":
    pass
