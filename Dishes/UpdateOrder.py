from flask import request, make_response
from flask_restful import Resource
from datetime import datetime
import ValidateUser


class UpdateOrder(Resource):
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

        if not (role in ["manager", "chef]"]):
            return make_response("Only client can make order", 403)
        if not (params.get('order_id')):
            return make_response("Identify order id", 400)
        if not (params.get('status')):
            return make_response("Identify order status", 400)
        status = params['status']
        if not (status in ["expecting", "processing", "done", "canceled"]):
            return make_response("Wrong order status choose from: expecting, processing, done, canceled", 400)

        dt = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        self.cur.execute("UPDATE 'order' SET status = (?), updated_at = (?)  WHERE id = (?)",
                         (status, dt, int(params['order_id']),))

        return "status changed", 200
