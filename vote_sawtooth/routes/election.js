const { addElection, allElection, deleteElection } = require('../controllers/election');

const router = require('express').Router();

router.post('/add', addElection)
router.get('/all', allElection)
router.post('/delete', deleteElection)

module.exports = router;