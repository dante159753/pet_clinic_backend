# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
app = Flask(__name__)
api = Api(app)

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

