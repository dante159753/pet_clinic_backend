# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, abort
from backend.util import generate_token
from backend.models.user import UserHelper
from backend.models.manager import ManagerHelper

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        parser.add_argument('is_manager', default=False)
        args = parser.parse_args()

        print args

        helper = UserHelper

        if args['is_manager'] == 'true':
            helper = ManagerHelper

        if helper.check_password(args['username'], args['password']):
            print helper.get_by_name(args['username'])
            return generate_token(helper.get_by_name(args['username']))
        else:
            return abort(401)