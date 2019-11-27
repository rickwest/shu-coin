![SHUcoin](ui/src/assets/logo.png)

A Python 🐍 blockchain and cryptocurrency project built as part of my Distributed Programming and Technologies module at Sheffield Hallam University.

---

## Task

*Develop a prototype application that demonstrates the practical application of some of the distributed programming techniques and technologies that you have studied during the module.* 

Based on personal interests, I decided to use this project as an opportunity to learn more about blockchain and how it works. 

I initially considered building a project that simply leveraged an existing blockchain network, such as a chat application using a library such as [LotionJS](https://lotionjs.com/), but I came to the conclusion that building my own blockchain would give me a better understanding of how the underlying technology works.

It was then suggested that to understand the benefits of a distributed, decentralised blockchain, building an application utilising the blockchain would be most beneficial. This lead to me building a simple crytocurrency that utilises the blockchain to keep a distributed, immutable ledger of transactions. Thus S(heffield) H(allam) U(niversity)coin was born! 
 
--- 

## Getting started 

### Requirements
To run this project, you will need python3 with pip and npm installed on your machine.


Make sure you have Python and that it’s available from your command line by simply running:

```
python --version
```

Additionally, you’ll need to make sure you have pip available. You can check this by running:

```
pip --version
```

Finally, ensure that you have npm installed by running: 

```
npm --version
```

### Installing the project

You can install this project by either downloading the source code or using git to clone the repository:

```
git clone https://github.com/rickwest/shu-coin.git
```

### Virtual Environment

The recommended way of developing Python applications and isolating their dependencies is through the use of a virtual environment.
`virtualenv` is a tool for creating these environments. `virtualenv` creates a folder which contains all the necessary executables to use the packages that a Python project would need.

If you don't already have virtualenv installed, you can install it by running the command:

```
pip install virtualenv
```

Test your installation:

```
virtualenv --version
```
---
 
## Installing the project dependencies
 
### Create a virtualenv for this project

With the project downloaded and `virtualenv` installed, you can create an environment for this project b running the following commands:

``` 
cd project_folder
virtualenv venv
```

virtualenv venv will create a folder in the current directory which will contain the Python executable files, and a copy of the pip library which you can use to install other packages. The name of the virtual environment (in this case, it was venv).

### Activate the virtualenv for this project and install the Python dependencies

Activate the virtual environment with the following comming:

```
source venv/bin/activate
```

With the virtual environment now active, you can install the project dependencies:

```
pip install -r requirements.txt
```

### Install the JavaScript dependencies

As well as installing the Python dependencies for this project, in order to run the ui, you will also need to install the JavaScript dependencies using `NPM`. From the project root directory, execute the following:

```
cd ui
npm install
```

---

## Running the application

### Run the API

To run the application, first you will need to run the Flask development server. From the root directory of the project, simply execute the `app.py` file:

```
python app.py 
``` 

**This command will start a master-node running on the default port 5000. To start further API nodes, you will need to execute the file with the peer argument. For example:**

```
python app.py peer
```

Running the command with the `peer` argument will start the development server on a new port and also synchronise the new node with the running master-node

### Run the frontend

To run the frontend React application you need to navigate into the `ui` directory of the project and start the server.

**You also need to specify the port of the API that you would like to connect to.**

```
cd ui
REACT_APP_SERVER_PORT={port number of API to connect to} npm start

// For example:
REACT_APP_SERVER_PORT=5000 npm start
```
--- 

## Tests

The important functionality of the project is unit tested. You can run the test suite by executing the following command from the root directory of the project:

```
python3 -m unittest
```

---

## Usage

### The Ui

Cryptocurrency networks, such as the Bitcoin, usually comprise of 4 different types of nodes; full nodes, super nodes, light nodes, and mining nodes.

This simple implementation, however, consists of only one type of node. 

Every node in this project has a copy of the full blockchain, it's own wallet and is able to mine transactions.

For interacting with the SHUcoin API the ui application, built with [React](https://reactjs.org/), provides a convenient way to explore the blockchain, create transactions and mine new blocks. 

### Video Demonstration

There is a video demonstration of the application available here: https://www.loom.com/share/c8134f3cfd7e4d80add162a862b01c73

### Basic Concepts

This project is the application of a simple distributed, decentralized cryptocurrency utilizing an underlying blockchain for the immutable store of data. I have covered some of the basic concepts inplemented in the project below:

#### Blockchain
The basic concept of blockchain is quite simple. A blockchain is a distributed database that maintains a continuously growing list of ordered records (blocks).

#### Proof of work
Proof of work introduces a computational puzzle that needs to be solved before a block can be added to the blockchain. Trying to solve this puzzle is commonly known as “mining”.
When a block is mined, the new block is broadcast too all the nodes in the network so that they can update there own blockchain.

Proof-of-work also enables us to approximately control the rate in which blocks can be added to the blockchain. 
This is done by changing the difficulty of the puzzle. If blocks are mined too often, the difficulty of the puzzle will increase and vice versa.

#### Transactions
Transactions are what turns the blockchain project into a cryptocurrency and enables the sending of coins from one address to another, assuming that we can show a proof that we own them in the first place.

#### Transaction Pool
The transaction pool (also known as “mempool” in bitcoin). stores transactions that are not yet included in the blockchain. In bitcoin, these transaction are also known as “unconfirmed transactions”. 
Typically, when someone wants to include a transaction to the blockchain, the transaction is broadcast to the network and hopefully some node will mine the transaction to the blockchain.
This feature is very important for a working cryptocurrency, since it means you don’t need to mine a block yourself, in order to include a transaction to the blockchain.

#### Wallet
The goal of the wallet is to act as an address interface for the cryptocurrency. Just like in a cryptocurrency like Bitcoin, you send coins to user wallent addresses and publish your own wallet address where other people can send coins.

--- 

## References

Hartikka, L. (2017). Naivecoin: a tutorial for building a cryptocurrency. Retrieved 26 November 2019, from https://lhartikk.github.io/

Van Flymen, D. (2019). Learn Blockchains by Building One. Retrieved 26 November 2019, from https://medium.com/@vanflymen/learn-blockchains-by-building-one-117428612f46

Nakamoto, S. (2008) Bitcoin: A Peer-to-Peer Electronic Cash System. https://bitcoin.org/bitcoin.pdf