#!/usr/bin/python3
# Entry point of the app
import os
import requests
import json
import datetime as dt

from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from collections import Counter

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = '7aee9ddbefc8fbae84a2913cdba46d95f6ec38519d0f694d'


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

#Adds a new user via API call
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

#Logs in a user via API call
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

#Sends a vote to the blockchain via API
def send_vote(cand_id):
    vote="ELE"+session['election-id']+"VID"+session['id_number']+"CID"+cand_id+"ELExx2022"
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

#Returns all votes from the blockchain
def test_all_votes():
    try:
        data = requests.get('http://localhost:8008/state')
    except Exception as exc:
        print(exc)
        data = None

    return data

#Gets data on a pending vote from the blockchain
def get_vote_data(link):
    try:
        data = requests.get(link)
    except Exception as exc:
        print(exc)
        data = None

    return data 

#Gets all candidates via API call
def add_candidate(payload):
    try:
        data = requests.post('http://localhost:8080/candidate/add', json=payload)
    except Exception as exc:
        print(exc)
        data = "Data not found"

    return data

#Get's a single candidate from API
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

# Add candidate via API
def find_all_candidates(elec_id):
    payload = {
        'election_id': elec_id
    }

    try:
        data = requests.get('http://localhost:8080/candidate/all', json=payload)
    except Exception as exc:
        print(exc)
        data = None
    return data

def find_all_candidates_admin():
    try:
        data = requests.get('http://localhost:8080/candidate/index')
    except Exception as exc:
        print(exc)
        data = None
    return data

#Get all users
def find_all_users():
    try:
        data = requests.get('http://localhost:8080/auth/all')
    except Exception as exc:
        print(exc)
        data = None
    return data

#Get all elections
def find_all_elections():
    try:
        data = requests.get('http://localhost:8080/election/all')
    except Exception as exc:
        print(exc)
        data = None
    return data

def find_one_election():
    try:
        payload = {
            "election_id": session['election-id']
        }
        data = requests.post('http://localhost:8080/election/get', json=payload)
    except Exception as exc:
        print(exc)
        data = None
    return data

#Add election
def add_election(payload):
    try:
        data = requests.post('http://localhost:8080/election/add', json=payload)
    except Exception as exc:
        print(exc)
        data = None
    return data

# End election
def end_election(payload):
    try:
        data = requests.post('http://localhost:8080/election/end', json=payload)
    except Exception as exc:
        print(exc)
        data = None
    return data

# Start afresh
def start_afresh():
    try:
        data = requests.post('http://localhost:8080/election/refresh')
    except Exception as exc:
        print(exc)
        data = None
    return data

def logout_func():
    session.pop('token', None)
    session.pop('username', None)
    session.pop('vote-link', None)
    session.pop('id_number', None)
    session.pop('election-id', None)
    flash('You logged out successfully')

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

        #If log in is successful a token is received
        #Then we can set session variables
        if 'access_token' in resp:
            session['id_number'] = resp['id_number']
            session['token'] = resp['access_token']
            session['username'] = username
            flash('Logged in successfully')
            return redirect(url_for('elections'))
        else:
            flash('Wrong username or password')
            return redirect(url_for('login_page'))
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
            flash('Registered successfully. Kindly log in.')
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

@app.route('/elections', methods=('GET', 'POST'))
def elections():
    # Getting all elections
    try:
        elecs = find_all_elections().json()
    except Exception as exc:
        print(exc)
        elecs = "Error getting elections"
        print(elecs)

    return render_template('elections.html', elecs=elecs)


@app.route('/vote/<id>', methods=('GET', 'POST'))
def vote(id):

    #Setting election id to session
    session['election-id'] = id

    if request.method == 'POST':
        voted_cand_id = request.form['voted-cand-id']

        try:
            # 1. Getting all votes to check if user has already voted
            resp = test_all_votes().json()
        except Exception as exc:
            print(exc)
            return "Error getting votes"

        if 'id_number' not in session:
            flash('Kindly register and login before voting')
            return(redirect(url_for('login_page')))

        votes_list = resp['data']
        arr_votes = []
        arr_elecs = []
        for i in range(1, len(votes_list)):
            voter_id = votes_list[i].get('data')[30:38]
            elec_id = votes_list[i].get('data')[3:27]

            if(session['id_number'] == voter_id and session['election-id'] == elec_id):
                flash("You have already voted. Kindly wait for the final results.")
                return redirect(url_for('results'))


        # 2. Vote check
        if 'id_number' not in session:
            flash('Kindly register and login before voting')
            return(redirect(url_for('login_page')))

        else:
            try:
                # 3. If no vote found, then now we send a vote
                resp = send_vote(voted_cand_id).json()
            except json.JSONDecodeError as exc:
                flash("Please log in.")
                return redirect(url_for('login_page'))
            except AttributeError as exc:
                flash("Error sending vote. You are not logged in.")
                return redirect(url_for('login'))

            # 4. If vote sent, then we get vote data
            if 'link' in resp:
                link = resp['link']
                vote_status = get_vote_data(link).json()

                session['vote-link'] = link
                return redirect(url_for('confirm'))
            else:
                flash("Error connecting to DB. Please contact the system administrator.")
                return redirect(url_for('elections'))

    # Get candidates if GET /vote
    else:
        #-------------------------------
        # Find candidates by election ID
        #-------------------------------
        try:
            resp = find_all_candidates(session['election-id'])
            resp_ = resp.json()
            print(resp_)
        except Exception as exc:
            print(exc)
            resp_ = "Error getting candidates"

        try:
            elec = find_all_elections().json()['all_elecs']
        except Exception as exc:
            print(exc)
            elec = "There was an error getting the elections"

        # Election time countdown
        if (elec):
            end = dt.datetime.strptime(elec[0]['deadline'][:-5], '%Y-%m-%dT%H:%M:%S')
        else:
            flash("No elections running. Please contact your admin.")
            return redirect(url_for('login_page'))
        #End of countdown

        count = 0

        #return 'Welcome to voting page';
        return render_template('vote.html', cands=resp_, election=elec, end_time=end,count=count)


@app.route('/results', methods=('GET', 'POST'))
def results():
    if request.method == 'POST':
        if 'elec-done' in request.form:
            payload = {
                "election_name": request.form['name']
            }
            try:
                resp = end_election(payload).json()

            except Exception as exc:
                print(exc)
                resp = None

        elif 'afresh' in request.form:
            try:
                resp = start_afresh().json()

            except Exception as exc:
                print(exc)
                resp = None

            flash(resp['message'])
            logout_func()
            return redirect(url_for('login_page'))

    # 1. Get all profiles
    resp = test_all_votes().json()

    try:
        votes = resp
    except Exception as exc:
        print(exc)
        votes = "There was an error"
        return votes

    votes_list =votes['data']
    vote_count = 0;
    dict_vote = []
    cand_votes = []

    # 2. Extract data from votes by splicing the string
    for i in range(1, len(votes_list)):
        # voter_id = votes_list[i].get('data')
        elec_id = votes_list[i].get('data')[3:27]
        voter_id = votes_list[i].get('data')[30:38]
        cand_id = votes_list[i].get('data')[41:49]
        print(votes_list[i].get('data'))
        print(voter_id+" "+cand_id)

        if 'election-id' not in session:
            flash('Select an election')
            return(redirect(url_for('elections')))

        if elec_id == session['election-id']:
            try:
                cand_name = find_candidate(cand_id).json()['user']["name"]
                dict_vote.append(cand_name)
                vote_count += 1
            except KeyError:
                flash('No candidates or elections available.')
                return(redirect(url_for('results')))


    # 3. Count occurrences of each unique candidate name in the dictionary
    result = Counter(dict_vote)
    dict_ = {str(k):v for k,v in result.items()}
    print(dict_)

    # 4. Get all candidates and append their vote count to their details
    try:
        all_cands = find_all_candidates(session['election-id']).json()['all_candidates']
    except KeyError:
        flash('No elections running')
        return(redirect(url_for('elections')))

    try:
        all_user = find_all_users().json()['all_users']
    except Exception as exc:
        print(exc)
        all_user = "There was an error getting the user count"

    users_ = len(all_user)

    for i in range(len(all_cands)):
        if all_cands[i]['name'] in dict_:
            # 5. Where the appending happens
            all_cands[i]['count'] = dict_[all_cands[i]['name']]
        else:
            all_cands[i]['count'] = 0

    try:
        elec = find_one_election().json()['election']
    except Exception as exc:
        print(exc)
        elec = "There was an error getting the elections"

    # Election time countdown
    if (elec):
        end = dt.datetime.strptime(elec['deadline'][:-5], '%Y-%m-%dT%H:%M:%S')
    else:
        flash("No elections running. Please contact your admin.")
        return redirect(url_for('login_page'))
    #End of countdown

    # Returning all of the data
    return render_template('results.html',
        end_time=end,
        election=elec,
        votes=dict_,
        cands=all_cands,
        total=vote_count,
        user_count = users_,
        elec_id = elec_id)

# Admin routes

@app.route('/admin', methods=('GET', 'POST'))
def admin_home():
    if request.method == 'POST':
        # Add a new election
        if 'elec-form' in request.form:
            print(request.form)
            payload = {
                "name": request.form['name'],
                "deadline": request.form['deadline']
            }
            
            try:
                resp = add_election(payload).json()
                flash('Election added successfully.')

            except Exception as exc:
                print(exc)
                resp = "Error adding election"
                flash('Error adding election. Please try again')
                print(resp)


            return redirect(url_for('admin_home'))

        elif 'cand-form' in request.form:
            payload = {
                "id_number": request.form['id_no'],
                "name": request.form['name'],
                "party": request.form['party'],
                "position": request.form['position'],
                "county": request.form['county'],
                "email": request.form['email'],
                "election": request.form['election']
            }

            try:
                resp = add_candidate(payload).json()
                flash('Candidate added successfully.')
            except Exception as exc:
                print(exc)
                resp = "Error adding candidate"
                flash('Error adding candidate. Please try again')
                print(resp)

            return redirect(url_for('admin_home'))

    # Getting all candidates
    try:
        cands = find_all_candidates_admin().json()['all_candidates']
    except Exception as exc:
        print(exc)
        cands = "Error getting candidates"
        print(cands)

    # Getting all elections
    try:
        elecs = find_all_elections().json()
    except Exception as exc:
        print(exc)
        elecs = "Error getting elections"
        print(elecs)

    return render_template('admin/index.html', cands=cands, elecs=elecs)

# End admin routes

# Logout Route
@app.route('/logout')
def logout():
    # Destroying all sessions
    logout_func()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
