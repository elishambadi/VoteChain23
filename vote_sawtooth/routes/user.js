const router = require('express').Router();
const { registerUser, loginUser, allUser, findUser } = require('../controllers/user');

router.post('/register', registerUser)
router.post('/login', loginUser)
router.get('/all', allUser)
router.post('/find', findUser)

module.exports = router;