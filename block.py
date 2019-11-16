import time


class Block:
    """A unit of storage."""

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
        return Block(
            timestamp, last_block.hash, "{}-{}".format(timestamp, last_block.hash), data
        )

    @staticmethod
    def genesis():
        """Genesis Block"""
        return Block(time.time_ns(), "genesis_last_block_hash", "genesis_hash", [])


if __name__ == "__main__":
    pass
