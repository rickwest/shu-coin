import time
import json
import hashlib


class Block:
    """A unit of storage."""

    GENESIS = {
        "timestamp": 1,
        "last_hash": "a4dd70bc5bb3ac23bc3b829a3b37029d15c7530c318ffcff7f30691b498745df",
        "hash": "9725bdb821e618a50dbfe245a8c4b7c21f73ff0ee16480eb1c51f94344a40aa4",
        "data": [],
    }

    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return """
            timestamp: {}
            last hash: {}
            hash: {}
            data: {}
            """.format(
            self.timestamp, self.last_hash, self.hash, self.data
        )

    @staticmethod
    def mine(last_block, data):
        """Mines a block based on given last block and data."""
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = BlockHelper.hash(timestamp, last_hash, data)

        return Block(timestamp, last_hash, hash, data)

    @staticmethod
    def genesis():
        """Genesis Block"""
        return Block(**Block.GENESIS)


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
