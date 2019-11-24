from unittest import TestCase
from wallet.wallet import Wallet, STARTING_BALANCE
from blockchain.blockchain import Blockchain
from wallet.transaction import Transaction


class TestWallet(TestCase):
    def test_verify_valid_signature(self):
        data = {"SHUcoin": "Is the best new cryptocurrency"}

        wallet = Wallet()
        signature = wallet.sign(data)

        self.assertTrue(Wallet.verify(wallet.public_key, data, signature))

    def test_verify_invalid_signature(self):
        data = {"SHUcoin": "Is the best new cryptocurrency"}
        signature = Wallet().sign(data)

        # Pass an incorrect public key to verify method. This fails as the public key isn't a pair with the private key used to generate the signature.
        self.assertFalse(Wallet.verify(Wallet().public_key, data, signature))

    def test_calculate_balance(self):
        blockchain = Blockchain()
        wallet = Wallet()

        self.assertEqual(
            Wallet.calculate_balance(blockchain, wallet.address), STARTING_BALANCE
        )

        amount = 50
        transaction = Transaction(wallet, "recipient_address", amount)
        blockchain.add_block([transaction.serialize()])

        self.assertEqual(
            Wallet.calculate_balance(blockchain, wallet.address),
            STARTING_BALANCE - amount,
        )

        # Add some transactions where wallet receives an amount
        blockchain.add_block(
            [
                Transaction(Wallet(), wallet.address, 30).serialize(),
                Transaction(Wallet(), wallet.address, 75).serialize(),
            ]
        )

        self.assertEqual(
            Wallet.calculate_balance(blockchain, wallet.address),
            STARTING_BALANCE - amount + 30 + 75,
        )
