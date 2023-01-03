const express = require('express')
const app = express();
const user = require('./routes/user')
const jwt = require('jsonwebtoken')
const port = process.env.PORT || 8080;
const { SECRET } = require('./config');
const authMiddleware = require('./auth-middleware');
const vote = require('./routes/vote')
const cors = require('cors');
const candidate = require('./routes/candidate')

app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.use(cors({
    origin: 'http://localhost:5000',
    methods: ['GET','POST']
}));

app.get('/health', (req, res) => {
    res.json({
        message: "Running"
    })
})
app.use('/auth', user)

// Validate API tokens
app.use('/api', authMiddleware, vote)
app.use('/candidate', candidate)

const start = async () => {
    try {
        const mongoose = require('mongoose')
        await mongoose.connect('mongodb://localhost:27017/votechain');

        app.listen(port, '0.0.0.0', () => {
            console.log('Server is running here http://localhost:${port}/health')
        })
    } catch (error) {
        console.error('Failed to get server running', error);
    }
}

start();
