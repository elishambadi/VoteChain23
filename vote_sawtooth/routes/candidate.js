const { addCandidate, allCandidates } = require('../controllers/candidate');

const router = require('express').Router();

router.post('/add', addCandidate)
router.get('/all', allCandidates)

module.exports = router;