from blockchain.block import Block, BlockError
from wallet.transaction import Transaction, MINING_REWARD_INPUT
from wallet.wallet import Wallet


class Blockchain:
    """The blockchain class. A list of blocks."""

    def __init__(self):
        self.chain = [Block.genesis()]

    @property
    def genesis(self):
        return self.chain[0]

    @property
    def previous_block(self):
        return self.chain[-1]

    def add_block(self, data):
        self.chain.append(Block.mine(self.previous_block, data))

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

    def serialize(self):
        """Encode a Blockchain object chain as a string."""
        return [block.serialize() for block in self.chain]

    @staticmethod
    def deserialize(serialized_chain):
        """Return a Blockchain instance from serialized string."""
        blockchain = Blockchain()
        blockchain.chain = [Block.deserialize(block) for block in serialized_chain]
        return blockchain

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
            previous_block = blockchain[i - 1]
            Block.is_valid(previous_block, block)

        Blockchain.contains_valid_transactions(blockchain)

    @staticmethod
    def contains_valid_transactions(blockchain):
        """Validates a chains based on rules for transactions.
        - a transaction must only appear once in the chain
        - there can only be one mining reward transaction per block
        - each transaction must be valid
        """
        transaction_ids = set()
        for i in range(len(blockchain)):
            block = blockchain[i]

            has_mining_reward = False
            for serialized_transaction in block.data:
                transaction = Transaction.deserialize(serialized_transaction)

                if transaction.id in transaction_ids:
                    raise ContainsInvalidTransactionError(
                        "Chain contains a duplicate transaction. Transaction {} is duplicated.".format(
                            transaction.id
                        )
                    )

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    # If already true then block must contain two reward transactions
                    if has_mining_reward:
                        raise ContainsInvalidTransactionError(
                            "Block {} has multiple mining reward transactions.".format(
                                block.hash
                            )
                        )

                    has_mining_reward = True
                else:
                    # Validate correct balance based on blockchain to date
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = blockchain[0:i]

                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain, transaction.input["address"]
                    )

                    if historic_balance != transaction.input["amount"]:
                        raise ContainsInvalidTransactionError(
                            "Transaction {} contains an invalid input amount.".format(
                                transaction.id
                            )
                        )

                Transaction.is_valid(transaction)


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


class ContainsInvalidTransactionError(BlockchainError):
    """Exception raised for errors with transactions within the chain."""

    def __init__(self, message="Invalid transaction in chain."):
        self.message = message


if __name__ == "__main__":
    pass
