#!/usr/bin/env python3
"""
Project Name: flask-mailroom
File Name: main.py
Author: Travis Brackney
Class: Python 230 - Self paced online
Date Created 8/22/2019
Python Version: 3.7.2
"""

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donor, Donation, User

app = Flask(__name__)
# app.debug = True
app.secret_key = b'\x06\x01\xba\xaa!]D\x9a\xd2\x81Wr%@\xb7\xb1'

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/new_donation/', methods=['GET', 'POST'])
def new_donation():

    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
        except Exception as e:
            message = "Donor name not found"
            return render_template('new_donation.jinja2', error=message)
        # donor = Donor.select().where(Donor.name == request.form['donor_name']).get()
        try:
            donation = Donation(donor=donor, value=float(request.form['donation_amt']))
            donation.save()
        except ValueError:
            message = "Donation value must be a number"
            return render_template('new_donation.jinja2', error=message)
            return render_template('new_donation.jinja2', error="Donor name not found")


        return redirect(url_for('all'))

    else:
        return render_template('new_donation.jinja2')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.select().where(User.name == request.form['name']).get()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('new_donation'))

        return render_template('login.jinja2', error="Incorrect Username or Password")

    else:
        return render_template('login.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
