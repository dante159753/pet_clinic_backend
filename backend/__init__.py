# -*- coding: utf-8 -*-
from flask import Flask, make_response
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)

#@api.representation('application/json')
#def output_json(data, code, headers=None):
#    resp = make_response(json.dumps(data), code)
#    resp.headers.extend({
#            'Access-Control-Allow-Origin': '*', 
#            'Access-Control-Allow-Methods' : 'PUT,GET,POST,DELETE',
#            'Access-Control-Allow-Headers': 'token, X-Requested-With',
#            "Access-Control-Expose-Headers": 'Origin, X-Requested-With, Content-Type, Accept, token'
#    	})
#    return resp

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1324'
app.config['MYSQL_DATABASE_DB'] = 'petclinic'

# set jwt secret
app.config['JWT_SECRET'] = 'my_secret'
# set upload folder
app.config['UPLOAD_FOLDER'] = '/root/petclinic/pet_clinic_backend/data'

# connect to mysql
from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)

from resources.login import Login
api.add_resource(Login, '/login')

from resources.user import User
api.add_resource(User, '/user', '/user/<int:user_id>')

from resources.manager import Manager
api.add_resource(Manager, '/manager', '/manager/<int:manager_id>')

from resources.manager import Authority
api.add_resource(Authority, '/authority', '/manager/<int:manager_id>/authority')

from resources.worker import Worker
api.add_resource(Worker, '/worker', '/worker/<int:worker_id>')

from resources.department import Depart
api.add_resource(Depart, '/depart', '/depart/<int:depart_id>')

from resources.item import Item
api.add_resource(Item, '/depart/<int:depart_id>/item', '/depart/<int:depart_id>/item/<int:item_id>')

from resources.item import ItemType
api.add_resource(ItemType, '/item_type', '/item_type/<int:item_type_id>')

from resources.case import CaseInfo, Case, CaseType
api.add_resource(CaseInfo, '/caseinfo', '/caseinfo/<int:case_id>')
api.add_resource(Case, '/case/<int:case_id>')
api.add_resource(CaseType, '/case_type')

from resources.roleplay import RoleplayInfo, RoleplayPage, RoleplayPageInfo
api.add_resource(RoleplayInfo, '/roleplay')
api.add_resource(RoleplayPageInfo, '/roleplay/<int:role_id>/pageinfo')
api.add_resource(RoleplayPage, '/roleplay/<int:role_id>/page', '/roleplay/<int:role_id>/page/<int:pagination>')

from resources.picture import Picture
api.add_resource(Picture, '/picture', '/picture/<int:pic_id>')

from resources.video import Video
api.add_resource(Video, '/video', '/video/<int:video_id>')
