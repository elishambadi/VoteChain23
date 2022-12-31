const { actions } = require("../constants")
const { sendTransaction } = require("../service/transaction")

exports.place_vote = (req, res) => {

    const detail = req.body.detail

    const id = req.params.id;
    const payload = {
        id,
        owner: req.user.publicKey,
        actions: actions.place_vote,
        detail: detail
    }

    return sendTransaction(payload, req.user.publicKey).then((result) => {
        res.json(result.data)
    }).catch((err) => {
        res.send(err & err.response ? err.response.data : err).status(400)
    })
}