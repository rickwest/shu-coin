from unittest import TestCase
from blockchain.blockchain import (
    Blockchain,
    GenesisError,
    ChainReplacementError,
    ContainsInvalidTransactionError,
)
from blockchain.block import Block
from wallet.transaction import Transaction, TransactionSignatureError
from wallet.wallet import Wallet


class TestBlockchain(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        for i in range(4):
            self.blockchain.add_block(
                [Transaction(Wallet(), "recipient_address", i).serialize()]
            )

    def test_instance(self):
        self.assertEqual(Blockchain().genesis, Block.genesis())

    def test_get_previous_block(self):
        self.assertEqual(self.blockchain.previous_block, self.blockchain.chain[-1])

    def test_add_block(self):
        self.assertEqual(len(self.blockchain.chain), 5)

        self.blockchain.add_block("SHUcoin")

        self.assertEqual(len(self.blockchain.chain), 6)
        self.assertEqual(self.blockchain.previous_block.data, "SHUcoin")

    def test_is_valid(self):
        Blockchain.is_valid(self.blockchain.chain)

    def test_is_valid_bad_genesis(self):
        self.blockchain.chain[0].data = "Invalid data"

        with self.assertRaises(GenesisError):
            Blockchain.is_valid(self.blockchain.chain)

    def test_replace(self):
        # Create a new blockchain, only has genesis
        blockchain = Blockchain()

        # Try replacing chain with longer chain
        blockchain.replace(self.blockchain.chain)

        # Assert that chain was replaced by longer one
        self.assertEqual(blockchain.chain, self.blockchain.chain)

    def test_replace_incoming_not_longer(self):
        # Create a new blockchain, only has genesis
        incoming = Blockchain()

        with self.assertRaisesRegex(
            ChainReplacementError,
            "Cannot replace. Incoming chain must be longer than local chain.",
        ):
            # Try replacing chain with shorter chain
            self.blockchain.replace(incoming.chain)

    def test_replace_incoming_not_valid(self):
        # Create a new blockchain, only has genesis
        blockchain = Blockchain()

        self.blockchain.chain[1].data = "Some bad data"

        with self.assertRaises(ChainReplacementError):
            # Try replacing chain with shorter chain
            blockchain.replace(self.blockchain.chain)

    def test_contains_valid_transactions(self):
        Blockchain.contains_valid_transactions(self.blockchain.chain)

    def test_contains_valid_transactions_duplicate_transaction(self):
        transaction = Transaction(Wallet(), "recipient", 1).serialize()

        self.blockchain.add_block([transaction, transaction])

        with self.assertRaises(ContainsInvalidTransactionError):
            Blockchain.contains_valid_transactions(self.blockchain.chain)

    def test_contains_valid_transactions_duplicate_rewards(self):
        self.blockchain.add_block(
            [
                Transaction.reward(Wallet()).serialize(),
                Transaction.reward(Wallet()).serialize(),
            ]
        )
        # Block contains multiple reward transactions so we expect an exception
        with self.assertRaises(ContainsInvalidTransactionError):
            Blockchain.contains_valid_transactions(self.blockchain.chain)

    def test_contains_valid_transactions_bad_transaction(self):
        bad_transaction = Transaction(Wallet(), "recipient", 1)
        # Use same transaction output but signed by wrong wallet
        bad_transaction.input["signature"] = Wallet().sign(bad_transaction.output)

        self.blockchain.add_block([bad_transaction.serialize()])

        with self.assertRaises(TransactionSignatureError):
            Blockchain.contains_valid_transactions(self.blockchain.chain)

    def test_contains_valid_transactions_bad_historic_balance(self):
        wallet = Wallet()
        bad_transaction = Transaction(wallet, "recipient", 1)

        # Tamper with transaction, giving wallet a high amount
        bad_transaction.output[wallet.address] = 1000

        # Ensure input amount and transaction amount are still correct so validation doesn't fail at that point
        bad_transaction.input["amount"] = 1001

        # Re-sign
        wallet.sign(bad_transaction.output)

        self.blockchain.add_block([bad_transaction.serialize()])

        with self.assertRaises(ContainsInvalidTransactionError):
            Blockchain.contains_valid_transactions(self.blockchain.chain)
