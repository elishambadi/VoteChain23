const { actions } = require("../constants")
const { sendTransaction } = require("../service/transaction")

exports.place_vote = (req, res) => {

    const vote = req.body.vote

    const payload = {
        id: vote,
        actions: actions.place_vote
    }

    return sendTransaction(payload, req.user.publicKey).then((result) => {
        res.json(result.data)
    }).catch((err) => {
        res.send(err & err.response ? err.response.data : err).status(400)
    })
}