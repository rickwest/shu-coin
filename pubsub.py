from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from blockchain.blockchain import ChainReplacementError
from blockchain.block import Block

config = PNConfiguration()
config.subscribe_key = "sub-c-8c14c81a-0bd0-11ea-a44b-b207d7d0b791"
config.publish_key = "pub-c-307735e3-b97a-4f96-bebb-2d8befec899b"

BLOCK_CHANNEL = "BLOCK_CHANNEL"


class BlockListener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message):
        print("something here")
        if message.channel == BLOCK_CHANNEL:
            block = Block.deserialize(message.message)
            proposed_chain = self.blockchain.chain.copy()
            proposed_chain.append(block)
            try:
                self.blockchain.replace(proposed_chain)
                print("Chain replaced successfully")
            except ChainReplacementError as e:
                print(e.message)


class PubSub:
    """This class handles the PubNub publish/subscribe, which facilitates communication between the nodes in the blockchain network.
    """

    def __init__(self, blockchain):
        self.pubnub = PubNub(config)

        # Subscribe to channels
        self.pubnub.subscribe().channels([BLOCK_CHANNEL]).execute()
        self.pubnub.add_listener(BlockListener(blockchain))

    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """Broadcast a block to peer nodes"""
        self.publish(BLOCK_CHANNEL, block.serialize())


if __name__ == "__main__":
    pass
