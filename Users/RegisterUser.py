from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
import re
import uuid
import hashlib

email_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
password_reg = r'[A-Za-z0-9@#$%^&+=-_]{8,}'
username_reg = r'[A-Za-z0-9@#$%^&+=-_]{3,20}'
SECRET_WORD = "calculator"


class RegisterUser(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def post(self):
        params = request.get_json()
        if not (params.get('username') and params.get('password') and params.get('email') and params.get('role')):
            return make_response("Username, password, email, role fields shouldn't be empty.", 400)

        username = params['username']
        email = params['email']
        password = params['password']
        role = params['role']

        if not (re.fullmatch(email_reg, email)):
            return make_response("Uncorrected email", 500)

        print(username)
        if not (re.fullmatch("^[a-zA-Z0-9_.-]+$", username)):
            return make_response(
                "Uncorrected username. Use username with: A-Z; a-z; 0-9; @#$%^&+=-_ and length 3-20 symbols", 500)

        if not(re.fullmatch(password_reg, password)):
            return make_response("Uncorrected password. Use password with symbols from: A-Z; a-z; 0-9; @#$%^&+=-_ and "
                                 "at least 8 symbols")

        if not (role in ["chef", "manager", "client"]):
            return make_response("Unavailable role. Select from this: 'chef', 'manager', 'client'", 500)

        if self.cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone():
            return make_response("This username is already taken. Select another one.", 500)
        if self.cur.execute("SELECT email FROM users WHERE email = ?", (email,)).fetchone():
            return make_response("User with email is already registered", 500)

        salt = uuid.uuid4().hex.encode()
        password_hash = str(hashlib.sha256(password.encode() + salt).hexdigest()) + ':' + salt.decode()
        dt_now = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        self.cur.execute("INSERT INTO users (username, email, password_hash, role, created_at, updated_at) VALUES (?, "
                         "?, ?, ?, ?, ?)", (username, email, password_hash, role, dt_now, dt_now,))
        return make_response("User registered.", 200)
