from wallet.wallet import Wallet
from wallet.transaction import (
    Transaction,
    InsufficientFundsError,
    TransactionValuesError,
    TransactionSignatureError,
)
from unittest import TestCase


class TestTransaction(TestCase):
    def test_transaction(self):
        sender_wallet = Wallet()
        recipient = "richard_west"
        amount = 100
        transaction = Transaction(sender_wallet, recipient, amount)

        # Assert that transaction output contains the correct recipient amount
        self.assertEqual(transaction.output[recipient], amount)

        # Assert that transaction output contains the correct new/remaining balance of senders wallet
        self.assertEqual(
            transaction.output[sender_wallet.address], sender_wallet.balance - amount
        )

        # Assert a timestamp exists in the transaction input
        self.assertIn("timestamp", transaction.input)

        # Assert correct values in the transaction input
        self.assertEqual(transaction.input["amount"], sender_wallet.balance)
        self.assertEqual(transaction.input["address"], sender_wallet.address)
        self.assertEqual(transaction.input["public_key"], sender_wallet.public_key)

        # Verify the signature to ensure correctness
        self.assertTrue(
            Wallet.verify(
                transaction.input["public_key"],
                transaction.output,
                transaction.input["signature"],
            )
        )

    def test_transaction_amount_exceeds_balance(self):
        sender_wallet = Wallet()
        sender_wallet.balance = 50

        with self.assertRaises(InsufficientFundsError):
            Transaction(sender_wallet, "richard_west", 100)

    def test_transaction_update_amount_exceeds_balance(self):
        sender_wallet = Wallet()
        sender_wallet.balance = 50
        recipient_address = "richard_west"

        transaction = Transaction(sender_wallet, recipient_address, 40)

        with self.assertRaises(InsufficientFundsError):
            transaction.update(sender_wallet, recipient_address, 20)

    def test_transaction_update(self):
        sender_wallet = Wallet()
        first_recipient_address = "richard_west"
        first_recipient_amount = 25

        second_recipient_address = "jing_wang"
        second_recipient_amount = 25

        transaction = Transaction(
            sender_wallet, first_recipient_address, first_recipient_amount
        )

        # Update transaction
        transaction.update(
            sender_wallet, second_recipient_address, second_recipient_amount
        )

        # Assert that transaction output contains the correct first recipient amount
        self.assertEqual(
            transaction.output[first_recipient_address], first_recipient_amount
        )

        # Assert that transaction output contains the correct second recipients amount
        self.assertEqual(
            transaction.output[second_recipient_address], second_recipient_amount
        )

        # Assert that transaction output contains the correct new/remaining balance of senders wallet
        self.assertEqual(
            transaction.output[sender_wallet.address],
            sender_wallet.balance - first_recipient_amount - second_recipient_amount,
        )

        # Verify the signature to ensure correctness. This will have been resigned.
        self.assertTrue(
            Wallet.verify(
                transaction.input["public_key"],
                transaction.output,
                transaction.input["signature"],
            )
        )

        # Test sending an additional amount to the same recipient
        first_recipient_additional_amount = 25
        transaction.update(
            sender_wallet, first_recipient_address, first_recipient_additional_amount
        )

        # Assert that transaction output contains the correct first recipient amount
        self.assertEqual(
            transaction.output[first_recipient_address],
            first_recipient_amount + first_recipient_additional_amount,
        )

        # Assert that transaction output contains the correct new/remaining balance of senders wallet
        self.assertEqual(
            transaction.output[sender_wallet.address],
            sender_wallet.balance
            - first_recipient_amount
            - second_recipient_amount
            - first_recipient_additional_amount,
        )

        # Verify the signature to ensure correctness. This will have been resigned.
        self.assertTrue(
            Wallet.verify(
                transaction.input["public_key"],
                transaction.output,
                transaction.input["signature"],
            )
        )

    def test_is_valid(self):
        Transaction.is_valid(Transaction(Wallet(), "recipient_address", 100))

    def test_is_valid_bad_output_values(self):
        sender_wallet = Wallet()  # A wallet starts with default value of 1000
        recipient_address = "recipient_address"
        transaction = Transaction(sender_wallet, recipient_address, 100)
        # Replicates a sender trying to inflate own balance
        transaction.output[sender_wallet] = 9999

        with self.assertRaises(TransactionValuesError):
            Transaction.is_valid(transaction)

    def test_is_valid_bad_signature(self):
        sender_wallet = Wallet()
        recipient_address = "recipient_address"

        transaction = Transaction(sender_wallet, recipient_address, 100)
        # Corrupt signature. Same transaction output, but signature is from a different wallet.
        transaction.input["signature"] = Wallet().sign(transaction.output)

        with self.assertRaises(TransactionSignatureError):
            Transaction.is_valid(transaction)