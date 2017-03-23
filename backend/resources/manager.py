# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.manager import ManagerHelper
from backend.util import check_token

manager_fields = {
    'manager_id': fields.Integer,
    'manager_name': fields.String
}

class Manager(Resource):
    @marshal_with(manager_fields)
    @check_token
    def get(self, manager_id=None):
        result = None
        if manager_id is not None:
            result = ManagerHelper.get_by_id(manager_id)
        else:
            result = ManagerHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(manager_fields)
    @check_token
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if ManagerHelper.create_user(args['username'], args['password']):
            return ManagerHelper.get_by_name(args['username'])
        else:
            abort(400)

    @marshal_with(manager_fields)
    @check_token
    def put(self, manager_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not ManagerHelper.modify_username(manager_id, args['username']):
                success = False
        if args['password'] is not None:
            if not ManagerHelper.modify_password(manager_id, args['password']):
                success = False

        if not success:
            abort(400)
        
        return ManagerHelper.get_by_id(manager_id)

    @check_token
    def delete(self, manager_id):
        if ManagerHelper.delete_by_id(manager_id):
            return ''
        else:
            abort(400)
