from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
import ValidateUser


class AddDish(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def post(self):
        params = request.get_json()
        error, user_id = ValidateUser.vaildate(self.cur, params=params)
        user_id = self.cur.execute("SELECT id FROM users WHERE username = (?)", (params['username'],)).fetchone()

        if not user_id:
            return make_response(error, 401)

        user_id = user_id[0]
        role = self.cur.execute("SELECT role FROM users WHERE id = (?)", (user_id,)).fetchone()[0]
        if role != "chef":
            return make_response("Don't have permission", 403)
        dt = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

        if not(isinstance(params['quantity'], int) and (params['quantity'] >= 0) and
               isinstance(params['price'], (float, int)) and (params['price'] > 0)):
            return make_response("quantity should non-negative integer and price should be more than zero")
        self.cur.execute("INSERT INTO dish (name, description, price, quantity, created_at, updated_at) "
                         "VALUES (?, ?, ?, ?, ?, ?)", (params['name'], params['description'], params['price'],
                                                       params['quantity'], dt, dt,))
        return make_response("Dish added", 201)
