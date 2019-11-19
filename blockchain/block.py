import time
import json
import hashlib
from config import MINE_RATE


class Block:
    """A unit of storage."""

    GENESIS = {
        "timestamp": 1,
        "last_hash": "a4dd70bc5bb3ac23bc3b829a3b37029d15c7530c318ffcff7f30691b498745df",
        "hash": "9725bdb821e618a50dbfe245a8c4b7c21f73ff0ee16480eb1c51f94344a40aa4",
        "data": [],
        "difficulty": 3,
        "nonce": "genesis_nonce",
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


class BlockHelper:
    @staticmethod
    def hash(*args):
        """Return a hash of given arguments"""
        # convert each arg to a string and sort
        args = sorted([json.dumps(arg) for arg in args])

        data = "".join(args)

        return hashlib.sha256(data.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    pass
