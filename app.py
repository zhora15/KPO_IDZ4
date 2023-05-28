from flask import Flask
from flask_restful import Api
import sqlite3
from Users.AuthUser import AuthUser
from Users.RegisterUser import RegisterUser
from Dishes.AddDish import AddDish
from Dishes.AddOrder import AddOrder
from Users.InfoUser import InfoUser
from Dishes.GetMenu import GetMenu
from Dishes.UpdateDish import UpdateDish
from Dishes.UpdateOrder import UpdateOrder

con = sqlite3.connect("db.sqlite", check_same_thread=False, isolation_level=None)
cursor = con.cursor()

app = Flask(__name__)

api = Api(app)

api.add_resource(AuthUser, "/api/auth_user", resource_class_kwargs={'cursor': cursor}	)
api.add_resource(RegisterUser, "/api/register_user", resource_class_kwargs={'cursor': cursor})
api.add_resource(AddDish, "/api/add_dish", resource_class_kwargs={'cursor': cursor})
api.add_resource(AddOrder, "/api/add_order", resource_class_kwargs={'cursor': cursor})
api.add_resource(InfoUser, "/api/info_user", resource_class_kwargs={'cursor': cursor})
api.add_resource(GetMenu, '/api/get_menu', resource_class_kwargs={'cursor': cursor})
api.add_resource(UpdateDish, "/api/update_dish", resource_class_kwargs={'cursor': cursor})
api.add_resource(UpdateOrder, "/api/update_order", resource_class_kwargs={'cursor': cursor})
api.init_app(app)

if __name__ == '__main__':
	app.run(debug=True, port=5000, host="127.0.0.1")
