from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
import ValidateUser


class AddOrder(Resource):
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

        if role != "client":
            return make_response("Only client can make order", 403)

        if not(params.get('dishes')) or not(isinstance(params['dishes'][0], dict)):
            return make_response("Wrong format for dishes", 400)

        dt = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        if params.get('spec_req'):
            spec_req = params['spec_req']
        else:
            spec_req = ""
        order_id = self.cur.execute("INSERT INTO 'order' (user_id, status, special_requests, created_at, updated_at) VALUES (?, "
                         "?, ?, ?, ?) RETURNING id", (user_id, "expecting", spec_req, dt, dt,)).fetchone()[0]

        dishes = params['dishes'][0]
        for name in dishes.keys():
            amount = dishes[name]
            res = self.cur.execute("SELECT id, price, quantity FROM dish WHERE name = (?)", (name,)).fetchone()
            if res is None:
                self.return_dishes(order_id)
                return make_response(name + " doesnt exists", 400)
            dish_id, price, quantity = res
            if amount <= 0:
                self.return_dishes(order_id)
                return make_response("Amount of dish should be more than zero", 400)
            if amount > quantity:
                self.return_dishes(order_id)
                return make_response(name + " not enough", 400)

            self.cur.execute("INSERT INTO order_dish (order_id, dish_id, quantity, price) VALUES (?, ?, ?, ?)", (order_id, dish_id, amount, price))
            self.cur.execute("UPDATE dish SET quantity = (?) WHERE id = (?)", (quantity - amount, dish_id,))
        return make_response("Order added", 201)

    def return_dishes(self, order_id):
        dishes = self.cur.execute("SELECT dish_id, quantity FROM order_dish WHERE order_id = (?)", (order_id, )).fetchall()
        for d in dishes:
            dish_id, amount = d
            quantity = self.cur.execute("SELECT quantity FROM dish WHERE id = (?)", (dish_id,)).fetchone()[0]
            self.cur.execute("UPDATE dish SET quantity = (?) WHERE id = (?)", (quantity + amount, dish_id,))
        self.cur.execute("DELETE FROM 'order' WHERE id = (?)", (order_id,))
