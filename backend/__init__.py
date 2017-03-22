# -*- coding: utf-8 -*-
from flask import Flask, make_response
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend({
    	"Access-Control-Allow-Origin": '*', 
    	"Access-Control-Expose-Headers": 'Origin, X-Requested-With, Content-Type, Accept, Access-Control-Allow-Origin, Access-Control-Allow-Methods',
    	"Access-Control-Allow-Methods": "POST, GET, OPTIONS, PUT, DELETE, HEAD"
    	})
    return resp

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1324'
app.config['MYSQL_DATABASE_DB'] = 'petclinic'

# connect to mysql
from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)

from resources.login import Login
api.add_resource(Login, '/login')

from resources.user import User
api.add_resource(User, '/user', '/user/<int:user_id>')

from resources.worker import Worker
api.add_resource(Worker, '/worker', '/worker/<int:worker_id>')

from resources.department import Depart
api.add_resource(Depart, '/department', '/department/<int:depart_id>')
