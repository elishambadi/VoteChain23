const addCandidateSchema = require('../validations/register-candidate')

const Candidate = require('../schemas/candidate')
const { SECRET } = require('../config');
const Election = require('../schemas/election');

exports.allCandidates = async (req, res) => {
    const all_candidates = await Candidate.find()
    return res.json({
        all_candidates: all_candidates
    })
}

exports.findCandidate = async (req, res) => {
    const one_cand = await Candidate.findOne({
        id_number: req.body.id_number
    })
    if (!one_cand){
        return res.json({"message":"Candidate not found"}).status(404)
    }
    return res.json({
        user: one_cand
    })
}

exports.addCandidate = async (req, res) => {
    const valid = addCandidateSchema.validate(req.body);
    if (valid.error) {
        return res.json(valid.error.details).status(400);
    }

    // Check if candidate exists using ID
    const cand = await Candidate.findOne({
        id_number: req.body.id_number
    })
    if (cand) {
        return res.status(409).json({
            message: "Candidate with ID already exists"
        })
    }

    // Parameters to be passed in the request
    const { id_number, email, name, party, position, county, election} = req.body;

    // Create a new user with the given values
    await Candidate.create({
        id_number,
        name,
        party,
        position,
        county,
        email,
        election
    })

    res.json({
        name,
        party,
        position,
        county,
        email
    })
}