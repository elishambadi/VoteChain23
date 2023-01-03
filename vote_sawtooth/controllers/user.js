const { createPrivateKey } = require('../service/credential')
const registerUserSchema = require('../validations/register-user')
const loginUserSchema = require('../validations/login-user')

const User = require('../schemas/user')
const jwt = require('jsonwebtoken');
const { SECRET } = require('../config');

exports.loginUser = async (req, res) => {
    const valid = loginUserSchema.validate(req.body)
    if (valid.error) {
        // Write a meaningful error message
        return res.json(valid.error.details).status(400);
    }
    
    const { username, password} = valid.value
    const user = await User.findOne({
        username,
        password
    });

    // console.log(user);

    if (!user) {
        return res.status(400).json({
            message: 'Username or password incorrect'
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

exports.allUser = async (req, res) => {
    const all_users = await User.find()
    return res.json({
        all_users: all_users
    })
}
exports.registerUser = async (req, res) => {
    const valid = registerUserSchema.validate(req.body);
    if (valid.error) {
        return res.json(valid.error.details).status(400);
    }

    // Check if user exists using ID number
    const user = await User.findOne({
        id_number: req.body.id_number
    })
    if (user) {
        return res.status(409).json({
            message: "User with ID already exists"
        })
    }

    const { privateKey, publicKey } = createPrivateKey();

    // Parameters to be passed in the request
    const { username, name, password, id_number, email } = req.body;

    // Create a new user with the given values
    await User.create({
        username,
        id_number,
        name,
        email,
        privateKey,
        publicKey,
        password
    })

    res.json({
        username,
        password,
        email,
        publicKey
    })
}
