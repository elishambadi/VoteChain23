const mongoose = require('mongoose')
const { Schema } = mongoose;

const candidateSchema = new Schema({
  id_number: String,
  name: String,
  party: String,
  position: String,
  county: String,
  email: String
});

const Candidate = mongoose.model('Candidate', candidateSchema)

module.exports = Candidate