from blockchain.block import Block, BlockError


class Blockchain:
    """The blockchain class. A list of blocks."""

    def __init__(self):
        self.chain = [Block.genesis()]

    @property
    def genesis(self):
        return self.chain[0]

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        self.chain.append(Block.mine(self.last_block, data))

    def replace(self, chain):
        """Replaces the local chain with the incoming one if:
        - incoming chain is longer than local chain
        - incoming chain is valid
        """

        if len(chain) <= len(self.chain):
            raise ChainReplacementError(
                "Cannot replace. Incoming chain must be longer than local chain."
            )

        try:
            Blockchain.is_valid(chain)
        except BlockError as e:
            raise ChainReplacementError("Cannot replace. {}".format(e.message))

        self.chain = chain

    def __repr__(self):
        return "SHUcoin Blockchain: {}".format(self.chain)

    @staticmethod
    def is_valid(blockchain):
        """Validates a blockchain.
           A blockchain must:
           - start with a genesis block
           - consist of only correctly formatted blocks
           """

        if blockchain[0] != Block.genesis():
            raise GenesisError()

        for i in range(1, len(blockchain)):
            block = blockchain[i]
            last_block = blockchain[i - 1]
            Block.is_valid(last_block, block)


class BlockchainError(Exception):
    """Base class for exceptions in this module."""

    pass


class GenesisError(BlockchainError):
    """Exception raised for errors with the genesis block of the blockchain."""

    def __init__(self, message="Invalid genesis block."):
        self.message = message


class ChainReplacementError(BlockchainError):
    """Exception raised for errors with chain replacement."""

    def __init__(
        self, message="Incoming chain is invalid. Local chain cannot be replaced."
    ):
        self.message = message


if __name__ == "__main__":
    pass
