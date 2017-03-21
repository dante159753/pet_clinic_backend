# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.user import UserHelper

user_fields = {
    'user_id': fields.Integer,
    'user_name': fields.String
}

class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id=None):
        result = None
        if user_id is not None:
            result = UserHelper.get_by_id(user_id)
        else:
            result = UserHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if UserHelper.create_user(args['username'], args['password']):
            return UserHelper.get_by_name(args['username'])
        else:
            abort(400)

    @marshal_with(user_fields)
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not UserHelper.modify_username(user_id, args['username']):
                success = False
        if args['password'] is not None:
            if not UserHelper.modify_password(user_id, args['password']):
                success = False

        if not success:
            abort(400)
        
        return UserHelper.get_by_id(user_id)

    def delete(self, user_id):
        if UserHelper.delete_by_id(user_id):
            return ''
        else:
            abort(400)