from unittest import TestCase
from blockchain.block import Block
from config import MINE_RATE, SECONDS
import time


class TestBlock(TestCase):
    def test_mine(self):
        last_block = Block.genesis()
        data = "Test data"

        result = Block.mine(last_block, data)

        self.assertIsInstance(result, Block)
        self.assertEqual(result.data, data)
        self.assertEqual(result.last_hash, last_block.hash)
        self.assertEqual(result.hash[0 : result.difficulty], "0" * result.difficulty)

    def test_difficulty_when_block_mined_too_quickly(self):
        last_block = Block.mine(Block.genesis(), "Test data")

        # New block mined immediately, quicker than the MINE_RATE.
        mined_block = Block.mine(last_block, "Some more data")

        # Assert that difficulty has increased by increment of one
        self.assertEqual(mined_block.difficulty, last_block.difficulty + 1)

    def test_difficulty_when_block_mined_too_slowly(self):
        last_block = Block.mine(Block.genesis(), "Test data")

        time.sleep(MINE_RATE / SECONDS)

        # New block mined too slowly, slower that the MINE_RATE.
        mined_block = Block.mine(last_block, "Some more data")

        # Assert that difficulty has decreased by increment of one
        self.assertEqual(mined_block.difficulty, last_block.difficulty - 1)

    def test_mine_block_difficulty_not_less_than_1(self):
        last_block = Block.mine(Block.genesis(), "Test data")
        # Ensure last block difficulty is 1
        last_block.difficulty = 1

        time.sleep(MINE_RATE / SECONDS)

        # New block mined too slowly, slower that the MINE_RATE.
        mined_block = Block.mine(last_block, "Some more data")

        # Assert than even though the block mined slowly,
        # the difficulty is not decreased as it cannot be less than 1
        self.assertEqual(mined_block.difficulty, 1)

    def test_genesis(self):
        expected = Block(
            Block.GENESIS["timestamp"],
            Block.GENESIS["last_hash"],
            Block.GENESIS["hash"],
            Block.GENESIS["data"],
            Block.GENESIS["difficulty"],
            Block.GENESIS["nonce"],
        )

        result = Block.genesis()

        self.assertIsInstance(result, Block)

        self.assertEqual(expected.__dict__, result.__dict__)
