class TransactionPool:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, transaction):
        """Adds a transaction to the pool"""
        self.transactions[transaction.id] = transaction

    def get_transaction_for_address(self, recipient_address):
        for transaction in self.transactions.values():
            if transaction.input["address"] == recipient_address:
                return transaction

    def clear_transactions(self, blockchain):
        """Clear transactions from the transactions pool that have already been recorded on the blockchain"""
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction["id"] in self.transactions:
                    del self.transactions[transaction["id"]]

        self.transactions = {}

    def get_serialized_transactions(self):
        """Return the string representations of the Transactions in the TransactionPool"""
        return [transaction.serialize() for transaction in self.transactions.values()]
