const router = require('express').Router();
const { registerUser, loginUser, allUser } = require('../controllers/user');

router.post('/register', registerUser)
router.post('/login', loginUser)
router.get('/all', allUser)

module.exports = router;