# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, abort
from backend.util import generate_token
from backend.models.user import UserHelper

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        parser.add_argument('is_manager', type=bool, default=False)
        args = parser.parse_args()

        print args

        if UserHelper.check_password(args['username'], args['password']):
        	return generate_token(UserHelper.get_by_name(args['username']))
        else:
        	return abort(401)