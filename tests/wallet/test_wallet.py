from unittest import TestCase
from wallet.wallet import Wallet


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
