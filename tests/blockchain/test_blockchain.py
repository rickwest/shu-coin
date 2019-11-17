from unittest import TestCase
from blockchain.blockchain import Blockchain
from blockchain.block import Block


class TestBlockchain(TestCase):
    def test_instance(self):
        self.assertEqual(Blockchain().get_chain()[0].hash, Block.GENESIS["hash"])

    def test_get_last_block(self):
        blockchain = Blockchain()
        blockchain.add_block("data")
        blockchain.add_block("last block data")

        self.assertEqual(blockchain.get_last_block().data, "last block data")

    def test_add_block(self):
        blockchain = Blockchain()

        self.assertEqual(len(blockchain.get_chain()), 1)

        blockchain.add_block("test data")

        self.assertEqual(len(blockchain.get_chain()), 2)
        self.assertEqual(blockchain.get_chain()[-1].data, "test data")
