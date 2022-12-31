const { TransactionHandler } = require('sawtooth-sdk-js/processor/handler')

const {
    InvalidTransaction,
    InternalError
} = require('sawtooth-sdk-js/processor/exceptions')

const { family, actions } = require('../constants');
const { hash } = require('../utils');

class VoteHandler extends TransactionHandler {
    constructor() {
        super(family.name, [family.version], [family.namespace])
    }

    async apply(transactionProcessRequest, context) {
        let payload;
        try {
            payload = JSON.parse(transactionProcessRequest.payload)
        } catch (error) {
            throw new InvalidTransaction('Error decoding payload')
        }
        console.log(payload.actions)

        if (!payload.actions){
            throw new InvalidTransaction('Invalid Action Type')
        }


        switch (payload.actions) {
            case actions.place_vote:
                // We will insert a Voter ID hash here to get a unique address per voter.
                // If address is same, block won't be added
                const address = family.namespace + hash(payload.id).slice(-64)

                const data = await context.getState([address]);

                // This code takes some time to run...
                // I suppose it checks the chole blockchain for addresses
                if(data && data[address] && data[address].length !== 0){
                    throw new InvalidTransaction('Existing vote found');
                }

                return context.setState({
                    [address]: payload.id
                }).then((addresses) => {
                    if (addresses.length === 0) {
                        throw new InvalidTransaction('State Error: Nothing got updated')
                    }
                })
        
            default:
                throw new InvalidTransaction('Invalid Action Type');
        }
    }
}

module.exports = VoteHandler