# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.worker import WorkerHelper
from backend.resources.department import depart_fields

job_fields = {
    'job_id': fields.Integer,
    'job_name': fields.String,
    'job_desc': fields.String
}

worker_fields = {
    'worker_id': fields.Integer,
    'worker_name': fields.String,
    'departments': fields.List(fields.Nested(depart_fields)),
    'job': fields.Nested(job_fields)
}

class Worker(Resource):
    @marshal_with(worker_fields)
    def get(self, worker_id=None):
        result = None
        if worker_id is not None:
            result = WorkerHelper.get_by_id(worker_id)
        else:
            result = WorkerHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(worker_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if WorkerHelper.create_user(args['username'], args['password']):
            return WorkerHelper.get_by_name(args['username'])
        else:
            abort(400)

    @marshal_with(worker_fields)
    def put(self, worker_id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help='username is required')
        parser.add_argument('password', required=False, help='password is required')
        args = parser.parse_args()

        print args
        success = True
        if args['username'] is not None:
            if not WorkerHelper.modify_username(worker_id, args['username']):
                success = False
        if args['password'] is not None:
            if not WorkerHelper.modify_password(worker_id, args['password']):
                success = False

        if not success:
            abort(400)
        
        return WorkerHelper.get_by_id(worker_id)

    def delete(self, worker_id):
        if WorkerHelper.delete_by_id(worker_id):
            return ''
        else:
            abort(400)