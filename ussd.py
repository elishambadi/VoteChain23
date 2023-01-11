#!/usr/bin/python3

import requests

from flask import Flask, redirect, url_for, request, make_response

app = Flask(__name__)

# app.config['SECRET_KEY'] = '7aee9ddbefc8fbae84a2913cdba46d95f6ec38519d0f694d'

response = ""

@app.route('/', methods=('GET', 'POST'))
def ussd_callback():
    global response
    session_id = request.values.get('sessionId', None)
    service_code = request.values.get('serviceCode', None)
    phone_number = request.values.get('phoneNumber', None)
    text = request.values.get('text', "default")

    if text == "":
        response = "CON Welcome to VoteChain23.\n"
        response += "Please enter your ID number to verify your vote."
    elif text == "1":
        response = "END Thank you for verifying."

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)