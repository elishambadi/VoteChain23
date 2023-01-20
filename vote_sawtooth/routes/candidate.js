const { addCandidate, allElecCandidates, findCandidate, allCandidates } = require('../controllers/candidate');

const router = require('express').Router();

router.post('/add', addCandidate)
router.get('/all', allElecCandidates)
router.get('/index', allCandidates)
router.post('/find', findCandidate)

module.exports = router;