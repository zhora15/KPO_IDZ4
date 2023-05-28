from flask import request, make_response, jsonify
from flask_restful import Resource

import ValidateUser


class InfoUser(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def get(self):
        params = request.get_json()
        error, manager_id = ValidateUser.vaildate(self.cur, params=params)

        if not manager_id:
            return make_response(error, 401)

        role = self.cur.execute("SELECT role FROM users WHERE id = (?)", (manager_id,)).fetchone()[0]

        if role != "manager":
            return make_response("You don't have permission", 402)

        if not params.get('user_token'):
            return make_response("Identify user token", 400)
        user_id = self.cur.execute("SELECT user_id FROM session WHERE session_token = (?)",
                                   (params['user_token'],)).fetchone()

        if user_id is None:
            return make_response("No user with that token", 400)

        user_id = user_id[0]
        username, email, role, created_at, updated_at = self.cur.execute \
            ("SELECT username, email, role, created_at, updated_at FROM users WHERE id = (?)", (user_id,)).fetchone()

        return jsonify({"id": user_id, "username": username, "email": email, "role": role, "created_at": created_at,
                        "updated_at": updated_at})
