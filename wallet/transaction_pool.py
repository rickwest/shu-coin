class TransactionPool:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, transaction):
        """Adds a transaction to the pool"""
        self.transactions[transaction.id] = transaction

    def has_existing_transaction(self, recipient_address):
        for transaction in self.transactions.values():
            if transaction.input["address"] == recipient_address:
                return transaction
