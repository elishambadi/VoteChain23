const mongoose = require('mongoose')
const { Schema } = mongoose;

const userSchema = new Schema({
  username: String,
  id_number: String,
  name: String,
  password: String,
  email: String,
  privateKey: String,
  publicKey: String,
  created_at: Date
});

const User = mongoose.model('User', userSchema)

module.exports = User