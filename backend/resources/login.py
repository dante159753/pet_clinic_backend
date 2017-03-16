# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from backend.models.user import UserHelper

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        parser.add_argument('is_manager', type=bool, default=False)
        args = parser.parse_args()


        return str(UserHelper.get_all())