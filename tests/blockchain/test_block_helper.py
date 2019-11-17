from unittest import TestCase
from blockchain.block import BlockHelper


class TestBlockHelper(TestCase):
    def test_hash(self):
        # Assert that the same hash is returned for the same arguments, regardless of order.
        self.assertEqual(
            BlockHelper.hash("one", 2, [3]), BlockHelper.hash([3], "one", 2)
        )

        # Assert that correct hash is returned for given argument.
        self.assertEqual(
            BlockHelper.hash("A test argument"),
            "29ca063ac6a3d092967db6f6e4c96f00ddb7b173fd568d4f6ec3b65f63454572",
        )
