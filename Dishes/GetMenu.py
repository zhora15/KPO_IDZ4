from flask import request, make_response, jsonify
from flask_restful import Resource

import ValidateUser


class GetMenu(Resource):
    def __init__(self, **kwargs):
        self.cur = kwargs['cursor']

    def get(self):
        params = request.get_json()
        error, manager_id = ValidateUser.vaildate(self.cur, params=params)

        if not manager_id:
            return make_response(error, 401)

        dishes = self.cur.execute("SELECT name, description, price, quantity FROM dish")

        if dishes is None:
            return make_response("Menu is empty", 400)

        dishes = dishes.fetchall()
        all_dishes = list()
        for dish in dishes:
            name, description, price, quantity = dish
            if quantity > 0:
                all_dishes.append({name: [description, price, quantity]})
        return jsonify(all_dishes)
