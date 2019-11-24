from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet
from unittest import TestCase


class TestTransactionPool(TestCase):
    def test_add_transaction(self):
        transaction_pool = TransactionPool()
        transaction = Transaction(Wallet(), "recipient_address", 10)

        transaction_pool.add_transaction(transaction)

        self.assertIn(transaction.id, transaction_pool.transactions)
        self.assertEqual(transaction_pool.transactions[transaction.id], transaction)
