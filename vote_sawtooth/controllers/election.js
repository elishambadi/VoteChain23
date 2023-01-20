const { SECRET } = require('../config');
const Candidate = require('../schemas/candidate');
const Election = require('../schemas/election');
const User = require('../schemas/user');

exports.deleteElection = async (req, res) => {
    
    elec_name = req.body.election_name;

    const elec = await Election.findOneAndDelete({
        name: elec_name
    })

    if (!elec){
        return res.json({
            message: "No election with name "+elec_name+" found!"
        })
    }
    else{
        return res.json({
            message: "Election deleted successfully"
        })
    }
}

exports.allElection = async (req, res) => {
    const all_elecs = await Election.find()
    return res.json({
        all_elecs
    })
}

exports.oneElection = async (req, res) => {
    const one_elec = await Election.findById(req.body.election_id)
    return res.json({
        election: one_elec
    })
}

// Clears all collections to start a fresh election
exports.refreshAll = async (req, res) => {

    await Election.deleteMany({});

    await Candidate.deleteMany({});

    await User.deleteMany({});

    return res.json({
        "message": "System refreshed successfully"
    })
}

exports.endElection = async (req, res) => {
    const elec_name = req.body.election_name

    await Election.updateOne({name: elec_name}, {'status':'ended'});

    return res.json({
        "message":"Election ended successfully"
    })
}

exports.addElection = async (req, res) => {
    
    // Check if election exists using name
    const elec = await Election.findOne({
        name: req.body.name
    })
    if (elec) {
        return res.status(409).json({
            message: "Elec: "+req.body.name+" already exists!"
        })
    }

    // Parameters to be passed in the request
    const { name, deadline } = req.body;

    // Create a new election with the given values
    const today = new Date()
    await Election.create({
        name,
        deadline,
        created_at: today,
        status: "ongoing"
    })

    res.json({
        name,
        deadline,
        created_at: today,
        status: "ongoing"
    })
}
