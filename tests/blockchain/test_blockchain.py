from unittest import TestCase
from blockchain.blockchain import Blockchain, GenesisError, ChainReplacementError
from blockchain.block import Block


class TestBlockchain(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        for i in range(4):
            self.blockchain.add_block("block {}".format(i))

    def test_instance(self):
        self.assertEqual(Blockchain().genesis, Block.genesis())

    def test_get_last_block(self):
        self.assertEqual(self.blockchain.last_block, self.blockchain.chain[-1])

    def test_add_block(self):
        self.assertEqual(len(self.blockchain.chain), 5)

        self.blockchain.add_block("SHUcoin")

        self.assertEqual(len(self.blockchain.chain), 6)
        self.assertEqual(self.blockchain.last_block.data, "SHUcoin")

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

        # Assert that chain was reaplaced by longer one
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
