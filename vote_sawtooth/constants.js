const { hash } = require("./utils")

exports.actions = {
    place_vote: 'place_vote'
}

exports.namespace = {
    vote: hash('vote').substring(0,2)
}

exports.family = {
    name: 'elec-vote',
    namespace: hash('vote').substring(0,6),
    version: '1.0'
}