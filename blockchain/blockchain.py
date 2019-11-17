from blockchain.block import Block


class Blockchain:
    """The blockchain class. A list of blocks."""

    def __init__(self):
        self.__chain = [Block.genesis()]

    def get_chain(self):
        return self.__chain

    def get_last_block(self):
        return self.__chain[-1]

    def add_block(self, data):
        self.__chain.append(Block.mine(self.get_last_block(), data))

    def __repr__(self):
        return "SHUcoin Blockchain: {}".format(self.__chain)


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block("test1")
    blockchain.add_block("test2")
    print(blockchain)
