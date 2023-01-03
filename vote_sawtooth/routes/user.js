const router = require('express').Router();
const { registerUser, loginUser, allUser } = require('../controllers/user');

router.post('/register', registerUser)
router.post('/login', loginUser)
router.post('/all', allUser)

module.exports = router;