#!/usr/bin/python3
# Entry point of the app
import os
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] =\
           'mysql:///root:Spidey43##@localhost:3306/votechain'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

# Voter Model
class Voter(db.Model):
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    id_number = db.Column(db.Integer, nullable=False, primary_key=True)
    province = db.Column(db.String(20), nullable=True)
    voted = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    vote_time = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f'<Student {self.id_number}>'


#dummy or sample voter data for demo
voters = [
    {
    'Name': 'John Doe',
    'ID': '1398749',
    'Province':'nairobi',
    'vote status': 'not yet'
    },
    {
    'Name': 'Martha Tim',
    'ID': '1428749',
    'Province':'western',
    'vote status': 'not yet'
    },
    {
    'Name': 'JAboyami Adike',
    'ID': '1300024',
    'Province':'rift valley',
    'vote status': 'not yet'
    }
]
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    #return 'Welcome to login page';
    return render_template('index.html')

@app.route('/register')
def register():
    #return 'Welcome to register page';
    return render_template('register.html')

@app.route('/profile')
def profile():
    #return 'Welcome to login page';
    return render_template('profile.html', voters=voters)

@app.route('/vote')
def vote():
    #return 'Welcome to voting page';
    return render_template('vote.html')

@app.route('/results')
def results():
    resp = test_all_votes().json()

    try:
        votes = resp
    except Exception as exc:
        print(exc)
        text = "There was an error"
    return render_template('results.html', votes=votes)

#@app.route('/{username}/profile')
#def user_profile():
    #return 'Welcome to your profile';
 #   return render_template('profile.html')



if __name__ == "__main__":
    app.run(debug=True)
