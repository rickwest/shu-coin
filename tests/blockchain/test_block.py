from unittest import TestCase
from blockchain.block import Block


class TestBlock(TestCase):
    def test_mine(self):
        last_block = Block.genesis()
        data = "Test data"

        result = Block.mine(last_block, data)

        self.assertIsInstance(result, Block)
        self.assertEqual(result.data, data)
        self.assertEqual(result.last_hash, last_block.hash)

    def test_genesis(self):
        expected = Block(
            Block.GENESIS["timestamp"],
            Block.GENESIS["last_hash"],
            Block.GENESIS["hash"],
            Block.GENESIS["data"],
        )

        result = Block.genesis()

        self.assertIsInstance(result, Block)

        self.assertEqual(expected.__dict__, result.__dict__)
