const { createPrivateKey } = require('../service/credential')
const registerUserSchema = require('../validations/register-user')
const loginUserSchema = require('../validations/login-user')

const User = require('../schemas/user')
const jwt = require('jsonwebtoken');
const { SECRET } = require('../config');

exports.loginUser = async (req, res) => {
    const valid = loginUserSchema.validate(req.body)
    if (valid.error) {
        return res.json(valid.error.details).status(400);
    }
    const {username, password} = valid.value
    const user = await User.findOne({
        username,
        password,
    })
    if (!user) {
        return res.status(400).json({
            message: "Username or password wrong"
        })
    }

    const { publicKey } = user;
    const token = jwt.sign({
        username,
        publicKey
    }, SECRET, {
        expiresIn: '1800s'
    })
    return res.json({
        access_token: token
    })
}

exports.registerUser = async (req, res) => {
    const valid = registerUserSchema.validate(req.body);
    if (valid.error) {
        return res.json(valid.error.details).status(400);
    }

    const user = await User.findOne({
        username: req.body.username
    })
    if (user) {
        return res.status(409).json({
            message: "User already exists"
        })
    }

    const { privateKey, publicKey } = createPrivateKey();
    const { username, name } = req.body;

    await User.create({
        username,
        name,
        privateKey,
        publicKey
    })

    res.json({
        name,
        username,
        publicKey
    })
}
