const Joi = require('joi');

//Data validation
const schema = Joi.object({
    username: Joi.string()
        .required(),
    password: Joi.string()
        .required()
})

module.exports = schema