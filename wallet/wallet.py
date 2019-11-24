import uuid
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    encode_dss_signature,
    decode_dss_signature,
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

STARTING_BALANCE = 10000  # Wallet starting balance, because we're kind like that!


class Wallet:
    """A wallet for a miner in the network. Keeps track of the balance and enables a miner to authorise transactions.
    """

    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data):
        """Generates a signature from the private key and data"""
        return decode_dss_signature(
            self.private_key.sign(
                json.dumps(data).encode("utf-8"), ec.ECDSA(hashes.SHA256())
            )
        )

    def serialize_public_key(self):
        self.public_key = self.public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

    @staticmethod
    def verify(public_key, data, signature):
        """Verify a signature based on the original public key and data."""
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode("utf-8"), default_backend()
        )
        try:
            deserialized_public_key.verify(
                encode_dss_signature(signature[0], signature[1]),
                json.dumps(data).encode("utf-8"),
                ec.ECDSA(hashes.SHA256()),
            )
            return True
        except InvalidSignature as e:
            return False

    @staticmethod
    def calculate_balance(blockchain, address):
        """Calculate balance of an address, based on transaction data in the blockchain
        Balance is the sum of all the output values since the most recent transaction by that address.
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction["input"]["address"] == address:
                    # When an address conducts a transaction it resets it balance
                    balance = transaction["output"][address]
                elif address in transaction["output"]:
                    balance += transaction["output"][address]

        return balance


if __name__ == "__main__":
    pass
