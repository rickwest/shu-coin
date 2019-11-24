import uuid
import time
from wallet.wallet import Wallet

MINING_REWARD = 50
MINING_REWARD_INPUT = {"address": "⛏️---SHUcoin-mining-reward---💰"}


class Transaction:
    """Represents an exchange of currency between wallets."""

    def __init__(
        self,
        sender_wallet=None,
        recipient_address=None,
        amount=None,
        id=None,
        output=None,
        input=None,
    ):
        self.id = id or str(uuid.uuid4())
        self.output = output or self.create_output(
            sender_wallet, recipient_address, amount
        )

        # Create a data structure that represents the input data for the transaction.
        # Signs the transaction and include the senders public key and wallet address.
        self.input = input or {
            "timestamp": time.time_ns(),
            "amount": sender_wallet.balance,
            "address": sender_wallet.address,
            "public_key": sender_wallet.public_key,
            "signature": sender_wallet.sign(self.output),
        }

    def create_output(self, sender_wallet, recipient_address, amount):
        """
        Create a data structure that represents the output data for the transaction.

        :param sender_wallet:
        :param recipient_address: The recipients wallet address.
        :param amount: The transaction amount
        :return: A dictionary representation of the output.
        """

        if amount > sender_wallet.balance:
            raise InsufficientFundsError()

        return {
            recipient_address: amount,
            sender_wallet.address: sender_wallet.balance - amount,
        }

    def update(self, sender_wallet, recipient_address, amount):
        """Updates the transaction with an existing or new recipient"""

        # Can only create or amend a transaction based on the value of the pending balance
        if amount > self.output[sender_wallet.address]:
            raise InsufficientFundsError()

        if recipient_address in self.output:
            # Add the additional amount to the existing recipient_address
            self.output[recipient_address] = self.output[recipient_address] + amount
        else:
            # Add another recipient and assign the amount
            self.output[recipient_address] = amount

        # Deduct additional amount from sender balance
        self.output[sender_wallet.address] = self.output[sender_wallet.address] - amount

        # Update timestamp and re-sign with the updated output
        self.input["timestamp"] = time.time_ns()
        self.input["signature"] = sender_wallet.sign(self.output)

    def serialize(self):
        """Encode Transaction object as a string."""
        return self.__dict__

    @staticmethod
    def deserialize(serialized_transaction):
        """Return a Transaction instance from serialized string."""
        return Transaction(**serialized_transaction)

    @staticmethod
    def is_valid(transaction):
        """Validates a transaction"""
        output_total = sum(transaction.output.values())

        if transaction.input == MINING_REWARD_INPUT:
            if list(transaction.output.values()) != [MINING_REWARD]:
                raise MiningRewardError()
            # return if mining reward is valid.
            return

        if transaction.input["amount"] != output_total:
            raise TransactionValuesError()

        if not Wallet.verify(
            transaction.input["public_key"],
            transaction.output,
            transaction.input["signature"],
        ):
            raise TransactionSignatureError()

    @staticmethod
    def reward(miner_wallet):
        """Generate a transaction to reward the miner."""
        return Transaction(
            input=MINING_REWARD_INPUT, output={miner_wallet.address: MINING_REWARD}
        )


class TransactionError(Exception):
    """Base class for exceptions in this module."""

    pass


class InsufficientFundsError(TransactionError):
    """Exception raised for errors with attempted transactions from wallets with insufficient funds."""

    def __init__(
        self,
        message="Insufficient funds. Transaction amount exceeds senders wallet balance.",
    ):
        self.message = message


class TransactionValuesError(TransactionError):
    """Exception raised when validating a transaction and the values are incorrect."""

    def __init__(
        self,
        message="Invalid transaction values. The sum of the output values are not equal to the input amount.",
    ):
        self.message = message


class TransactionSignatureError(TransactionError):
    """Exception raised when a transaction signature in invalid."""

    def __init__(self, message="Invalid transaction signature."):
        self.message = message


class MiningRewardError(TransactionError):
    """Exception raised when a mining reward transaction in invalid."""

    def __init__(self, message="Invalid mining reward."):
        self.message = message


if __name__ == "__main__":
    pass
