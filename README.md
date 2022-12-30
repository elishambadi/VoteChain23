# VoteChain
VoteChain is an online, blockchain voting platform with the goal of increasing the credibility of democracy and making
voting available from home.

## How to run the program

To run the program, make app.py executable.

Run app.py as a script and access on the browser.

Sawtooth blockchain is run from the vote-_sawtooth folder.

To run the blockchain, ensure you are in the blockchain folder. Then run two commands in different tabs:

`docker -f sawtooth-compose.yaml up` - To start the blockchain validator server 

`npm run dev` -
To start the node server than interfaces with the blockchain

At this point your infrastructure is up, you can write some application code, or use the sample application in test.js file.

Command: `npm run test`

The test.js file adds some sample data to the blockchain. Before data is added, it must be organized as below.

Data - Transaction - Batch then sent to the block.

All these stages are seen in the test.js file.

To view the current blockchain: visit https://localhost:8080/state.
