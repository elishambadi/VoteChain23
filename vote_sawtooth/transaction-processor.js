const {TransactionProcessor} = require('sawtooth-sdk-js/processor')
const IntegerKeyHandler = require('./handler/intkey')
const VALIDATOR_URL = 'tcp://localhost:4004'
const transactionProcessor = new TransactionProcessor(VALIDATOR_URL)

//Adding a transaction handler

transactionProcessor.addHandler(new IntegerKeyHandler())

transactionProcessor.start()

//Keyboard interrupt for safe shutdown
process.on('SIGUSR2', () => {
    transactionProcessor.handleShutdown();
})
