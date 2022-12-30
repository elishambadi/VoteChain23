const { randomBytes, createHash } = require('crypto')
const secp256k1 = require('secp256k1')

const axios = require('axios').default;

const { Secp256k1PrivateKey } = require('sawtooth-sdk-js/signing/secp256k1')
const { CryptoFactory, createContext } = require('sawtooth-sdk-js/signing')

const protobuf = require('sawtooth-sdk-js/protobuf')

const createPrivateKey = () => {
  const msg = randomBytes(32)
  let privKey
  do {
    privKey = randomBytes(32)
  } while (!secp256k1.privateKeyVerify(privKey))
  const pubKey = secp256k1.publicKeyCreate(privKey)
  const sigObj = secp256k1.ecdsaSign(msg, privKey)
  console.log(secp256k1.ecdsaVerify(sigObj.signature, msg, pubKey))
  return privKey.toString('hex')
}

const privateKeyHexStr = createPrivateKey();

const privateKey = new Secp256k1PrivateKey(Buffer.from(privateKeyHexStr, 'hex'));

const context = createContext('secp256k1');

const signer = new CryptoFactory(context).newSigner(privateKey);

//Prepare a payload / Data to be stored
//Payload > Transaction > TransactionList > Batch > BatchList > Bytes > REST_API

const payload = "Voter-ID:4549829, Governor: A05"
const payloadBytes = Buffer.from(payload);

const transactionHeaderBytes = protobuf.TransactionHeader.encode({
    familyName: 'intkey',
    familyVersion: '1.0',
    inputs: ['1cf126'],
    outputs: ['1cf126'],
    signerPublicKey: signer.getPublicKey().asHex(),
    nonce: `${Math.random()}`,
    batcherPublicKey: signer.getPublicKey().asHex(),
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
    signerPublicKey: signer.getPublicKey().asHex(),
    transactionIds: transactions.map(t => t.headerSignature)
}).finish();

const batch = protobuf.Batch.create({
    header: batchHeaderBytes,
    headerSignature: signer.sign(batchHeaderBytes),
    transactions: transactions
})

const batches = [batch ];

console.log(batches)

const batchListBytes = protobuf.BatchList.encode({
    batches: batches
}).finish();

console.log(batchListBytes.toString())

// AXIOS

axios.post('http://localhost:8008/batches', batchListBytes, {
    headers: {
        'Content-Type': 'application/octet-stream'
    },
    data: batchListBytes
}).then((res) => {
    console.log(res.data);
}).catch((err) => {
    console.log(err.response)
})
