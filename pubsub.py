from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from blockchain.blockchain import ChainReplacementError
from blockchain.block import Block
from wallet.transaction import Transaction

config = PNConfiguration()
config.subscribe_key = "sub-c-8c14c81a-0bd0-11ea-a44b-b207d7d0b791"
config.publish_key = "pub-c-307735e3-b97a-4f96-bebb-2d8befec899b"

BLOCK_CHANNEL = "BLOCK_CHANNEL"
TRANSACTION_CHANNEL = "TRANSACTION_CHANNEL"


class BlockListener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message):
        if message.channel == BLOCK_CHANNEL:
            block = Block.deserialize(message.message)
            proposed_chain = self.blockchain.chain.copy()
            proposed_chain.append(block)
            try:
                self.blockchain.replace(proposed_chain)
                self.transaction_pool.clear_transactions(self.blockchain)
                print("Chain replaced successfully 👌")
            except ChainReplacementError as e:
                print(e.message)


class TransactionListener(SubscribeCallback):
    def __init__(self, transaction_pool):
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message):
        if message.channel == TRANSACTION_CHANNEL:
            transaction = Transaction.deserialize(message.message)
            self.transaction_pool.add_transaction(transaction)
            print("Transaction added to the pool successfully 👌")


class PubSub:
    """This class handles the PubNub publish/subscribe, which facilitates communication between the nodes in the blockchain network.
    """

    def __init__(self, blockchain, transaction_pool):
        self.pubnub = PubNub(config)

        # Subscribe to channels
        self.pubnub.subscribe().channels([BLOCK_CHANNEL, TRANSACTION_CHANNEL]).execute()

        # Add listeners
        self.pubnub.add_listener(BlockListener(blockchain, transaction_pool))
        self.pubnub.add_listener(TransactionListener(transaction_pool))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """Broadcast a block to peer nodes"""
        self.publish(BLOCK_CHANNEL, block.serialize())

    def broadcast_transaction(self, transaction):
        """Broadcast a transaction to peer nodes"""
        self.publish(TRANSACTION_CHANNEL, transaction.serialize())


if __name__ == "__main__":
    pass
