const Joi = require('joi');

//Data validation
const schema = Joi.object({
    id_number: Joi.number(),
    name: Joi.string().min(10).required(),
    party: Joi.string().max(50),
    position: Joi.string().max(50),
    county: Joi.string().max(50),
    email: Joi.string().max(50)
})

// Some of this validation is done on Flask side

module.exports = schema