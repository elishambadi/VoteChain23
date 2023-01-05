const { addCandidate, allCandidates, findCandidate } = require('../controllers/candidate');

const router = require('express').Router();

router.post('/add', addCandidate)
router.get('/all', allCandidates)
router.post('/find', findCandidate)

module.exports = router;