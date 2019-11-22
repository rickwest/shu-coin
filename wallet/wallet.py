import uuid
import json
from config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """A wallet for a miner in the network. Keeps track of the balance and enables a miner to authorise transactions.
    """

    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """Generates a signature from the private key and data"""
        return self.private_key.sign(
            json.dumps(data).encode("utf-8"), ec.ECDSA(hashes.SHA256())
        )

    @staticmethod
    def verify(public_key, data, signature):
        """Verify a signature based on the original public key and data."""
        try:
            public_key.verify(
                signature, json.dumps(data).encode("utf-8"), ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature as e:
            return False


if __name__ == "__main__":
    pass
