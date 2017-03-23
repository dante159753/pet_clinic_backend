# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.manager import ManagerHelper, AuthorityHelper
from backend.util import check_token

manager_fields = {
    'manager_id': fields.Integer,
    'manager_name': fields.String
}

authority_fields = {
    'authority_id': fields.Integer,
    'authority_desc': fields.String
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


class Authority(Resource):
    @marshal_with(authority_fields)
    @check_token
    def get(self, manager_id = None):
        result = None
        if manager_id:
            result = AuthorityHelper.get_by_manager_id(manager_id)
        else:
            result = AuthorityHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(authority_fields)
    @check_token
    def put(self, manager_id):
        parser = reqparse.RequestParser()
        parser.add_argument('auth_list', action='append', required=True, help='auth_list is required')
        args = parser.parse_args()

        if not ManagerHelper.get_by_id(manager_id):
            return abort(404, 'can not find manager_id')

        origin_auth_ids = map(
            lambda x: str(x['authority_id']), 
            AuthorityHelper.get_by_manager_id(manager_id)
            )

        origin_set = set(origin_auth_ids)
        dest_set = set(args['auth_list'])
        print origin_set, dest_set

        # in desc but not in origin, need to add
        for auth_id in dest_set - origin_set:
            AuthorityHelper.add_authority(manager_id, auth_id)

        # in origin but not in desc, need to remove
        for auth_id in origin_set - dest_set:
            AuthorityHelper.remove_authority(manager_id, auth_id)
        
        
        return AuthorityHelper.get_by_manager_id(manager_id)

