const { addElection, allElection, deleteElection, endElection, refreshAll, oneElection } = require('../controllers/election');

const router = require('express').Router();

router.post('/add', addElection)
router.get('/all', allElection)
router.post('/delete', deleteElection)
router.post('/end', endElection)
router.post('/get', oneElection)

router.post('/refresh', refreshAll)

module.exports = router;