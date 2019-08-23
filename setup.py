#!/usr/bin/env python3
"""
Project Name: flask-mailroom
File Name: model.py
Author: Travis Brackney
Class: Python 230 - Self paced online
Date Created 8/22/2019
Python Version: 3.7.2
"""


import random

from model import db, Donor, Donation, User
from passlib.hash import pbkdf2_sha256

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation, User])

db.create_tables([Donor, Donation, User])

alice = Donor(name="Alice")
alice.save()

bob = Donor(name="Bob")
bob.save()

charlie = Donor(name="Charlie")
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

User(name="admin", password=pbkdf2_sha256.hash("password")).save()
User(name="jim", password=pbkdf2_sha256.hash("llpaintit")).save()
