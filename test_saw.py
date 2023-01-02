#!/usr/bin/python3
#This is some code to test the Sawtooth API

import requests
from flask import Flask

app = Flask(__name__)

API_KEY = '12345abcXYZ'

def query_api_register(username, name, password):
    try:
        payload = {
            "username": username,
            "name": name,
            "password": password
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

def test_api():
    try:
        data = requests.get('http://localhost:8080/health')
    except Exception as exc:
        print(exc)
        data = None

    return data

def test_vote():
    try:
        headers = {
            "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRpbGlzbzEiLCJwdWJsaWNLZXkiOiIwMjliYzI3MDcyZTFhNGRiZGEwNmU0MWU3ZTYxNTMwMjNmMTkyOGVlZjNhOTE2Njk4ZDZhYWNkMjQ1ODkzNDJhODciLCJpYXQiOjE2NzI2NjU0NTEsImV4cCI6MTY3MjY2NzI1MX0.4n_uOcf1T6Ae1XBzPW5QUZBbnLE6aPJC2GGdkIO2ASU'
        }
        vote_info = {
            "vote":"VID:2211G:G115"
        }
        data = requests.post('http://localhost:8080/api/vote', json=vote_info, headers=headers)

    except Exception as exc:
        print(exc)
        data = None

    return data

@app.route('/test', methods=["GET"])
def test_api_route():
    resp = test_api().json()

    try:
        text = resp['message']
    except Exception as exc:
        print(exc)
        text = "There was an error."
    return text

@app.route('/test-register', methods=["GET", "POST"])
def result_register():
    resp = query_api_register("Tiliso1", "elisha", "123pass").json()

    try:
        text = resp['name'] + " "+resp['username']+" "+resp['publicKey']
    except:
        text = "There was an error."
    return text

@app.route('/test-login', methods=["GET", "POST"])
def result_login():
    resp = query_api_login("Tiliso1", "123pass").json()

    try:
        text = resp['access_token']
    except:
        text = "There was an error."
    return text

@app.route('/test-vote', methods=["GET", "POST"])
def test_vote_api():
    resp = test_vote().json()

    try:
        text = resp['link']
    except Exception as exc:
        print(exc)
        text = "There was an error."
    return text
    
if __name__ == '__main__':
    app.run(debug=True)     