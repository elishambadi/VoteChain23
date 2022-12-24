#!/usr/bin/python3
# Entry point of the app
from flask import Flask, redirect, url_for, render_template, request, flash
app = Flask(__name__, static_folder='static')


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
    return render_template('login.html')

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
    #return 'Welcome to results page';
    return render_template('results.html')

#@app.route('/{username}/profile')
#def user_profile():
    #return 'Welcome to your profile';
 #   return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)
