from wallet.transaction import Transaction
from wallet.transaction_pool import TransactionPool
from wallet.wallet import Wallet
from unittest import TestCase
from blockchain.blockchain import Blockchain


class TestTransactionPool(TestCase):
    def test_add_transaction(self):
        transaction_pool = TransactionPool()
        transaction = Transaction(Wallet(), "recipient_address", 10)

        transaction_pool.add_transaction(transaction)

        self.assertIn(transaction.id, transaction_pool.transactions)
        self.assertEqual(transaction_pool.transactions[transaction.id], transaction)

    def test_clear_transaction(self):
        transaction_pool = TransactionPool()

        transaction1 = Transaction(Wallet(), "recipient_address", 1)
        transaction2 = Transaction(Wallet(), "recipient_address", 2)

        transaction_pool.add_transaction(transaction1)
        transaction_pool.add_transaction(transaction2)

        blockchain = Blockchain()
        blockchain.add_block([transaction1.serialize(), transaction2.serialize()])

        self.assertIn(transaction1.id, transaction_pool.transactions)
        self.assertIn(transaction2.id, transaction_pool.transactions)

        transaction_pool.clear_transactions(blockchain)

        self.assertNotIn(transaction1.id, transaction_pool.transactions)
        self.assertNotIn(transaction2.id, transaction_pool.transactions)
