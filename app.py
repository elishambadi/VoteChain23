#!/usr/bin/python3
# Entry point of the app
import os
import requests
import json
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import Counter

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = '7aee9ddbefc8fbae84a2913cdba46d95f6ec38519d0f694d'

# app.config['SQLALCHEMY_DATABASE_URI'] =\
#            'mysql:///root:Spidey43##@localhost:3306/votechain'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# db = SQLAlchemy(app)

# # Voter Model
# class Voter(db.Model):
#     first_name = db.Column(db.String(20), nullable=True)
#     last_name = db.Column(db.String(20), nullable=True)
#     id_number = db.Column(db.Integer, nullable=False, primary_key=True)
#     province = db.Column(db.String(20), nullable=True)
#     voted = db.Column(db.Integer, nullable=True)
#     dob = db.Column(db.Date, nullable=True)
#     vote_time = db.Column(db.DateTime, nullable=True)
#     gender = db.Column(db.Integer, nullable=True)
#     email = db.Column(db.String(30), nullable=True)

#     def __repr__(self):
#         return f'<Student {self.id_number}>'


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

# Functions - To be moved to controller

def query_api_register(username, name, password, id_no, email):
    try:
        payload = {
            "username": username,
            "name": name,
            "password": password,
            "id_number": id_no,
            "email": email
        }
        data = requests.post('http://localhost:8080/auth/register', json=payload)
        print(data)
    except Exception as exc:
        print(exc)
        data = "Data not found"

    return data

def query_api_login(username, password):
    try:
        payload = {
            "username": username,
            "password": password
        }
        data = requests.post('http://localhost:8080/auth/login', json=payload)
    except Exception as exc:
        print(exc)
        data = "Data not found"

    return data

def get_candidates():
    try:
        data = requests.get('http://localhost:8080/candidate/all')
    except Exception as exc:
        print(exc)
        data = "Data not found"

    return data

def send_vote(cand_id):
    vote="VID"+session['id_number']+"CID"+cand_id+"x2022"
    try:
        headers = {
            "Authorization": 'Bearer '+session['token']
        }
        vote_info = {
            "vote":vote
        }
        data = requests.post('http://localhost:8080/api/vote', json=vote_info, headers=headers)

    except Exception as exc:
        print(exc)
        data = None

    return data

def test_all_votes():
    try:
        data = requests.get('http://localhost:8008/state')
    except Exception as exc:
        print(exc)
        data = None

    return data

def get_vote_data(link):
    try:
        data = requests.get(link)
    except Exception as exc:
        print(exc)
        data = None

    return data 

def find_candidate(id_number):
    payload = {
        "id_number":id_number
    }
    try:
        data = requests.post('http://localhost:8080/candidate/find', json=payload)
    except Exception as exc:
        print(exc)
        data = None
    return data

def find_all_candidates():
    try:
        data = requests.get('http://localhost:8080/candidate/all')
    except Exception as exc:
        print(exc)
        data = None
    return data

def find_all_users():
    try:
        data = requests.get('http://localhost:8080/auth/all')
    except Exception as exc:
        print(exc)
        data = None
    return data

# End of functions

# Start of Routes

@app.route('/')
def home():
    return redirect(url_for('login_page'))

@app.route('/about')
def landing():
    #return 'Welcome to login page';
    return render_template('landing.html')

@app.route('/login', methods=('GET', 'POST'))
def login_page():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']

        resp = query_api_login(username, password).json()

        if 'access_token' in resp:
            session['id_number'] = resp['id_number']
            session['token'] = resp['access_token']
            session['username'] = username
            return redirect(url_for('vote'))
        else:
            return "Wrong username or password"
    else:
        #return 'Welcome to login page';
        return render_template('index.html')

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        id_no = request.form['id_no']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        # TODO: Fix server side validation
        # if not id_no:
        #     flash('ID Number is required')
        # elif not name:
        #     flash('Name is required')
        # elif not email:
        #     flash('Email is required')
        # elif not password:
        #     flash('Password is required')
        # elif not username:
        #     flash('Username is required')
        # else:
        #     # Send the content to the api
        #     return "Hello! : "+id_no+" "+name

        #Sending a request
        resp = query_api_register(username, name, password, id_no, email)
        
        if resp.status_code == 200:
            print("Voter {} registered successfully")
            print(resp.json())
            return redirect(url_for('login_page'))
        else:
            print(resp.status_code)
            return "Error encountered "+str(resp.status_code)

    else:
        #return 'Welcome to register page';
        return render_template('register.html')

@app.route('/profile')
def profile():
    #return 'Welcome to login page';
    return render_template('profile.html', voters=voters)

@app.route('/confirm', methods=('GET', 'POST'))
def confirm():
    #return 'Welcome to login page';

    link = session['vote-link']

    vote_status = get_vote_data(link).json()

    return render_template('confirm.html', resp=vote_status)

@app.route('/vote', methods=('GET', 'POST'))
def vote():

    if request.method == 'POST':
        voted_cand_id = request.form['voted-cand-id']

        try:
            resp = test_all_votes().json()
        except Exception as exc:
            print(exc)
            return "Error getting votes"

        votes_list =resp['data']
        dict_votes = []
        for i in range(1, len(votes_list)):
            # voter_id = votes_list[i].get('data')
            voter_id = votes_list[i].get('data')[3:11]
            dict_votes.append(voter_id)

        print(session['id_number'])
        print(dict_votes)

        if session['id_number'] in dict_votes:
            return "You have already voted. Kindly wait for the results"
        else:
            try:
                resp = send_vote(voted_cand_id).json()
            except json.JSONDecodeError as exc:
                return "Your web token has expired. Please login again."
            except AttributeError as exc:
                return "Error sending vote. You are not logged in."

            if 'link' in resp:
                link = resp['link']
                vote_status = get_vote_data(link).json()

                session['vote-link'] = link
                # return render_template('confirm.html', resp=vote_status)
                return redirect(url_for('confirm'))
            else:
                return "Error connecting to DB. Please contact the system administrator."

    # Get candidates
    else:
        resp = get_candidates().json()['all_candidates']

        #return 'Welcome to voting page';
        return render_template('vote.html', cands=resp)

@app.route('/results')
def results():
    resp = test_all_votes().json()

    try:
        votes = resp
    except Exception as exc:
        print(exc)
        votes = "There was an error"

    votes_list =votes['data']
    dict_vote = []
    cand_votes = []

    for i in range(1, len(votes_list)):
        # voter_id = votes_list[i].get('data')
        voter_id = votes_list[i].get('data')[9:16]
        cand_id = votes_list[i].get('data')[14:20]

        cand_name = find_candidate(cand_id).json()['user']["name"]

        dict_vote.append(cand_name)

    result = Counter(dict_vote)
    dict_ = {str(k):v for k,v in result.items()}
    print(dict_)

    vote_count = len(votes_list) - 1;

    all_cands = get_candidates().json()['all_candidates']

    try:
        all_user = find_all_users().json()['all_users']
    except Exception as exc:
        print(exc)
        all_user = "There was an error getting the user count"

    users_ = len(all_user)

    for i in range(len(all_cands)):
        if all_cands[i]['name'] in dict_:
            all_cands[i]['count'] = dict_[all_cands[i]['name']]
        else:
            all_cands[i]['count'] = 0

    return render_template('results.html',
        votes=dict_,
        cands=all_cands,
        total=vote_count,
        user_count = users_)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('username', None)
    session.pop('vote-link', None)
    session.pop('id_number', None)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
