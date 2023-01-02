const router = require('express').Router()
const { place_vote } = require('../controllers/transaction')

// A voter should post their ID number or unique number
router.post('/vote', place_vote);

module.exports = router