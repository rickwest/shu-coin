import time
import json
import hashlib

SECOND = 1000000000  # A second in nanoseconds
MINE_RATE = 4000000000  # Mine rate in nanoseconds (4 seconds)


class Block:
    """A unit of storage."""

    GENESIS = {
        "timestamp": 1,
        "last_hash": "00dd70bc5bb3ac23bc3b829a3b37029d15c7530c318ffcff7f30691b498745df",
        "hash": "0005bdb821e618a50dbfe245a8c4b7c21f73ff0ee16480eb1c51f94344a40aa4",
        "data": [],
        "difficulty": 3,
        "nonce": 0,
    }

    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return """
            timestamp: {}
            last hash: {}
            hash: {}
            data: {}
            difficulty: {}
            nonce: {}
            """.format(
            self.timestamp,
            self.last_hash,
            self.hash,
            self.data,
            self.difficulty,
            self.nonce,
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def serialize(self):
        """Encode Block object as a string."""
        return self.__dict__

    @staticmethod
    def deserialize(serialized_block):
        """Return a Block instance from serialized string."""
        return Block(**serialized_block)

    @staticmethod
    def mine(last_block, data):
        """
        Mines a block based on given last block and data.
        Mining is only complete when a block hash is found that meets the leading 0's requirement of proof of work.
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash

        difficulty = Block.regulate_difficulty(last_block, timestamp)
        nonce = 0

        hash = BlockHelper.hash(timestamp, last_hash, data, difficulty, nonce)

        while hash[0:difficulty] != "0" * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.regulate_difficulty(last_block, timestamp)
            hash = BlockHelper.hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():
        """Genesis Block"""
        return Block(**Block.GENESIS)

    @staticmethod
    def regulate_difficulty(last_block, new_timestamp):
        """Regulates the block difficulty based on the configured MINE_RATE.
        We increase the difficulty for blocks mined too quickly and decrease the difficulty for blocks mined slowly
        """
        difficulty = last_block.difficulty

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return difficulty + 1
        elif (difficulty - 1) > 0:
            return difficulty - 1
        else:
            return 1

    @staticmethod
    def is_valid(last_block, block):
        """Validates a block.
        A block must:
        - have the correct last hash
        - have correct number of leading zeros as per difficulty - proof of work requirement
        - only adjust difficulty by a value of 1
        - have a hash that is valid combo of block fields
        """
        if block.last_hash != last_block.hash:
            raise LastHashError()

        if block.hash[0 : block.difficulty] != "0" * block.difficulty:
            raise ProofOfWorkError()

        if abs(block.difficulty - last_block.difficulty) > 1:
            raise DifficultyDeviationError()

        reproduced_hash = BlockHelper.hash(
            block.timestamp, block.last_hash, block.data, block.difficulty, block.nonce
        )

        if block.hash != reproduced_hash:
            raise HashError()


class BlockHelper:
    @staticmethod
    def hash(*args):
        """Return a hash of given arguments"""
        # convert each arg to a string and sort
        args = sorted([json.dumps(arg) for arg in args])

        data = "".join(args)

        return hashlib.sha256(data.encode("utf-8")).hexdigest()


class BlockError(Exception):
    """Base class for exceptions in this module."""

    pass


class LastHashError(BlockError):
    """Exception raised for errors with the last block hash."""

    def __init__(self, message="Invalid last block hash."):
        self.message = message


class ProofOfWorkError(BlockError):
    """Exception raised for errors with the proof of work."""

    def __init__(self, message="Hash does not meet the proof of work requirement"):
        self.message = message


class DifficultyDeviationError(BlockError):
    """Exception raised for errors with difficulty deviation."""

    def __init__(self, message="Difficulty deviation is greater than permitted."):
        self.message = message


class HashError(BlockError):
    """Exception raised for errors with the block hash"""

    def __init__(self, message="Invalid block hash"):
        self.message = message


if __name__ == "__main__":
    pass
