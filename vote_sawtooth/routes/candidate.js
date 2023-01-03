const { addCandidate, allCandidates } = require('../controllers/candidate');

const router = require('express').Router();

router.post('/add', addCandidate)
router.post('/all', allCandidates)

module.exports = router;