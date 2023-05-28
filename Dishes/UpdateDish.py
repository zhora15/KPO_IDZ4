from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
import ValidateUser


class UpdateDish(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def patch(self):
        params = request.get_json()
        error, user_id = ValidateUser.vaildate(self.cur, params=params)
        user_id = self.cur.execute("SELECT id FROM users WHERE username = (?)", (params['username'],)).fetchone()

        if user_id is None:
            return make_response(error, 401)

        user_id = user_id[0]
        role = self.cur.execute("SELECT role FROM users WHERE id = (?)", (user_id,)).fetchone()[0]

        if role != "manager":
            return make_response("Only client can make order", 403)

        if not (params.get('name')):
            return make_response("Identify dish name", 400)

        res = self.cur.execute("SELECT id FROM dish WHERE name = (?)", (params['name'],)).fetchone()
        if res is None:
            return make_response("No dish with this name", 400)
        dish_id = res[0]

        if not (params.get('price') or params.get('quantity')):
            return make_response("Set price or quantity", 400)

        outp = ""
        if params.get('price'):
            if not (isinstance(params['price'], (float, int)) and (params['price'] > 0)):
                return make_response("price should be more than zero", 400)
            self.cur.execute("UPDATE dish SET price  = (?) WHERE id = (?)", (params['price'], dish_id,))
            outp += "price "
        if params.get('quantity'):
            if not (isinstance(params['quantity'], int) and (params['quantity'] >= 0)):
                return make_response("quantity should non-negative integer", 400)
            self.cur.execute("UPDATE dish SET quantity  = (?) WHERE id = (?)", (params['quantity'], dish_id,))
            outp += "quantity "
        dt = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        self.cur.execute("UPDATE dish SET updated_at = (?) WHERE id = (?)", (dt, dish_id))

        return make_response(outp + "changed", 200)
