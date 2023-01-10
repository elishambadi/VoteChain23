# VoteChain
VoteChain is an online, blockchain voting platform with the goal of increasing the credibility of democracy and making
voting available from home.

## How to run the program

To run the program, make app.py executable.

Run app.py as a script and access on the browser.

## Blockchain

Sawtooth blockchain is run from the vote-sawtooth folder.

To run the blockchain, ensure you are in the blockchain folder. Then run two commands in different tabs:

`docker -f sawtooth-compose.yaml up` - To start the blockchain validator server 

`npm run dev` -
To start the node server than interfaces with the blockchain

`npm run tp` - To start the transaction processor

`./app.py` - To run the Flask endpoint app if you didn't already run it.

The data flow is as below:
Flask app files -> NodeJSAPI -> (vote js route -> transaction js controller -> transaction js service -> elec_vote js handler). The role of each file is as below:

Vote Js - routes traffic to controller
Transaction JS controller - unpacks the request and sends data to the service
Transaction JS service - builds the data into a blockchain transaction
Elec_vote js - checks and sends the transaction to the blockchain

Meanwhile querying the blockchain is direct through: http://localhost:8008/state once the chain is running locally.
