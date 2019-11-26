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
REACT_APP_SERVER_PORT={port number of api to connect to} npm start

// For example:

REACT_APP_SERVER_PORT=5000 npm start
```
--- 

## Tests

The important functionality of the project is unit tested. You can run the test suite by executing the following command from the root directory of the project:

```
python3 -m unittest
```