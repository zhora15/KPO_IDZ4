from flask import request, make_response, jsonify
from flask_restful import Resource
import hashlib
import jwt
from datetime import datetime, timedelta

SECRET_WORD = "calculator"


class AuthUser(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def post(self):
        params = request.get_json()
        if not (params.get('username') or params.get('password')):
            return make_response("Username and password shouldn't be empty", 500)

        res = self.cur.execute("SELECT id, password_hash FROM users WHERE username = (?)",
                               (params['username'],)).fetchone()

        if (res is None) or (res[0] is None) or self.cmpPassword(res[1], params['password']):
            return make_response("Uncorrect username or password", 401)
        user_id = res[0]

        saved_jqt_token = self.cur.execute("SELECT session_token FROM session WHERE user_id = (?)",
                                           (user_id,)).fetchone()

        if saved_jqt_token:
            saved_jqt_token = saved_jqt_token[0]
            try:
                decoded_token = jwt.decode(saved_jqt_token, SECRET_WORD, algorithms=['HS256'])
                if int(decoded_token['user_id']) != user_id:
                    self.cur.execute("DELETE FROM session WHERE user_id = (?)", (int(decoded_token["user_id"]),))
                    return make_response("Stolen token", 401)
                return jsonify({'token': saved_jqt_token})
            except jwt.ExpiredSignatureError:
                pass
            except:
                return make_response("Internal error", 500)
        new_date = datetime.now() + timedelta(hours=12)
        jwt_token = jwt.encode({'user_id': str(user_id), 'exp': new_date}, SECRET_WORD, algorithm="HS256")

        if saved_jqt_token:
            self.cur.execute("UPDATE session SET session_token = (?), expires_at = (?) WHERE user_id = (?)",
                             (jwt_token, new_date.strftime('%m/%d/%Y, %H:%M:%S'), user_id,))
        else:
            self.cur.execute("INSERT INTO session (user_id, session_token, expires_at) VALUES (?, ?, ?)",
                             (user_id, jwt_token, new_date.strftime('%m/%d/%Y, %H:%M:%S'),))

        return jsonify({'token': jwt_token})

    def cmpPassword (self, password_hash, inp_password):
        password, salt = password_hash.split(':')
        return password != str(hashlib.sha256(inp_password.encode() + salt.encode()).hexdigest())