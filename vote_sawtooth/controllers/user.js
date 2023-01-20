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
    
    const { username, password } = valid.value
    const user = await User.findOne({
        username,
        password
    });

    // console.log(user);

    if (!user) {
        console.log("- Username or password incorrect. Or user inexistent.")
        return res.status(400).json({
            message: 'Username or password incorrect. Or user inexistent.'
        })
    }
    else{
        console.log("- Logging in user...")
    }

    const { publicKey } = user;
    const { id_number } = user;
    const token = jwt.sign({
        username,
        publicKey
    }, SECRET, {
        expiresIn: '1800s'
    })
    return res.json({
        id_number: id_number, 
        access_token: token
    })
}

exports.allUser = async (req, res) => {
    const all_users = await User.find()
    console.log("- Finding all users...")
    return res.json({
        all_users: all_users
    })
}

exports.findUser = async (req, res) => {
    const one_user = await User.findOne({
        id_number: req.body.id_number
    })
    if (!one_user){
        console.log('- User not found')
        return res.json({"message":"User not found"}).status(404)
    }
    else{
        console.log('- Finding user...')
    }
    return res.json({
        user: one_user
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
        console.log("- User already exists")
        return res.status(409).json({
            message: "User with ID already exists"
        })
    }
    else{
        console.log('- Creating user...')
    }

    const { privateKey, publicKey } = createPrivateKey();

    // Parameters to be passed in the request
    const { username, name, password, id_number, email } = req.body;

    // Create a new user with the given values
    const today = new Date()
    await User.create({
        username,
        id_number,
        name,
        email,
        privateKey,
        publicKey,
        password,
        created_at: today
    })

    res.json({
        username,
        password,
        email,
        publicKey
    })
}
