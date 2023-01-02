const { randomBytes, createHash } = require('crypto')
const secp256k1 = require('secp256k1')

const axios = require('axios').default;

const { Secp256k1PrivateKey } = require('sawtooth-sdk-js/signing/secp256k1')
const { CryptoFactory, createContext } = require('sawtooth-sdk-js/signing')

const protobuf = require('sawtooth-sdk-js/protobuf');
const { family, actions } = require('../constants');
const User = require('../schemas/user');
const { getSigner } = require('./credential');


const sendTransaction = async (payload, signerPublicKey) => {
    const user = await User.findOne({
        publicKey: signerPublicKey
    })
    if (!user) {
        throw new Error('User key does not exist')
    }

    const signer = getSigner(user.privateKey)

    const payloadBytes = Buffer.from(JSON.stringify(payload));

    const transactionHeaderBytes = protobuf.TransactionHeader.encode({
        familyName: family.name,
        familyVersion: family.version,
        inputs: ['9b416c'],
        outputs: ['9b416c'],
        signerPublicKey,
        nonce: `${Math.random()}`,
        batcherPublicKey: signerPublicKey,
        dependencies: [],
        payloadSha512: createHash('sha512').update(payloadBytes).digest('hex')
    }).finish();
    
    const transaction = protobuf.Transaction.create({
        header: transactionHeaderBytes,
        headerSignature: signer.sign(transactionHeaderBytes),
        payload: payloadBytes
    })
    
    const transactions = [transaction];
    
    const batchHeaderBytes = protobuf.BatchHeader.encode({
        signerPublicKey,
        transactionIds: transactions.map(t => t.headerSignature)
    }).finish();
    
    const batch = protobuf.Batch.create({
        header: batchHeaderBytes,
        headerSignature: signer.sign(batchHeaderBytes),
        transactions: transactions
    })
    
    const batches = [batch];
    
    // console.log(batches)
    
    const batchListBytes = protobuf.BatchList.encode({
        batches: batches
    }).finish();

    console.log("Data received. Posting now...")
    
    // AXIOS
    
    return result =  axios.post('http://localhost:8008/batches', batchListBytes, {
        headers: {
            'Content-Type': 'application/octet-stream'
        },
        data: batchListBytes
    });
}

module.exports = {
    sendTransaction
}