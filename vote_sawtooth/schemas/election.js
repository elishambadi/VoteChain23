const mongoose = require('mongoose')
const { Schema } = mongoose;

const electionSchema = new Schema({
  name: String,
  deadline: Date,
  created_at: Date,
  status: String
});

const Election = mongoose.model('Election', electionSchema)

module.exports = Election