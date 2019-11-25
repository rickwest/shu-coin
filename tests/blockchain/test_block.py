from unittest import TestCase
from blockchain.block import (
    Block,
    PreviousHashError,
    HashError,
    DifficultyDeviationError,
    ProofOfWorkError,
    MINE_RATE,
    SECOND,
)

import time


class TestBlock(TestCase):
    def setUp(self):
        self.previous_block = Block.genesis()
        self.block = Block.mine(self.previous_block, "SHUcoin")

    def test_mine(self):
        result = Block.mine(self.previous_block, "Bitcoin")

        self.assertIsInstance(result, Block)
        self.assertEqual(result.data, "Bitcoin")
        self.assertEqual(result.previous_hash, self.previous_block.hash)
        self.assertEqual(result.hash[0 : result.difficulty], "0" * result.difficulty)

    def test_difficulty_when_block_mined_too_quickly(self):
        previous_block = Block.mine(self.previous_block, "Ethereum")

        # New block mined immediately, quicker than the MINE_RATE.
        mined_block = Block.mine(previous_block, "Verge")

        # Assert that difficulty has increased by increment of one
        self.assertEqual(mined_block.difficulty, previous_block.difficulty + 1)

    def test_difficulty_when_block_mined_too_slowly(self):
        previous_block = Block.mine(self.previous_block, "TRX")

        time.sleep(MINE_RATE / SECOND)

        # New block mined too slowly, slower that the MINE_RATE.
        mined_block = Block.mine(previous_block, "Stellar")

        # Assert that difficulty has decreased by increment of one
        self.assertEqual(mined_block.difficulty, previous_block.difficulty - 1)

    def test_mine_block_difficulty_not_less_than_1(self):
        previous_block = Block.mine(self.previous_block, "Dragonchain")
        # Ensure previous block difficulty is 1
        previous_block.difficulty = 1

        time.sleep(MINE_RATE / SECOND)

        # New block mined too slowly, slower that the MINE_RATE.
        mined_block = Block.mine(previous_block, "Some more data")

        # Assert than even though the block mined slowly,
        # the difficulty is not decreased as it cannot be less than 1
        self.assertEqual(mined_block.difficulty, 1)

    def test_genesis(self):
        expected = Block(
            Block.GENESIS["timestamp"],
            Block.GENESIS["previous_hash"],
            Block.GENESIS["hash"],
            Block.GENESIS["data"],
            Block.GENESIS["difficulty"],
            Block.GENESIS["nonce"],
        )

        result = Block.genesis()

        self.assertIsInstance(result, Block)

        self.assertEqual(expected.__dict__, result.__dict__)

    def test_is_valid(self):
        # Block is valid if no exception is thrown
        Block.is_valid(self.previous_block, self.block)

    def test_is_valid_bad_previous_hash(self):
        # Set bad previous hash
        self.block.previous_hash = "Bad"

        with self.assertRaises(PreviousHashError):
            Block.is_valid(self.previous_block, self.block)

    def test_is_valid_bad_pow(self):
        self.block.hash = "fff"

        with self.assertRaises(ProofOfWorkError):
            Block.is_valid(self.previous_block, self.block)

    def test_is_valid_bad_difficulty(self):
        self.block.difficulty = 10
        # Set correct number of leading zeros to prevent pow error and ensure testing difficulty deviation.
        self.block.hash = "0" * self.block.difficulty

        with self.assertRaises(DifficultyDeviationError):
            Block.is_valid(self.previous_block, self.block)

    def test_is_valid_bad_hash(self):
        self.block.hash = "0" * self.block.difficulty + "dgfsdgfsgdfsgf"

        with self.assertRaises(HashError):
            Block.is_valid(self.previous_block, self.block)
