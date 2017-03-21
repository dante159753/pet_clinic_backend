# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.department import DepartHelper

depart_fields = {
    'depart_id': fields.Integer,
    'depart_name': fields.String,
    'depart_type': fields.Integer,
    'depart_desc': fields.String
}

class Depart(Resource):
    @marshal_with(depart_fields)
    def get(self, depart_id=None):
        result = None
        if depart_id is not None:
            result = DepartHelper.get_by_id(depart_id)
        else:
            result = DepartHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(depart_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('depart_name', required=True, help='depart_name is required')
        parser.add_argument('depart_type', required=True, help='depart_type is required')
        parser.add_argument('depart_desc', required=True, help='depart_desc is required')
        args = parser.parse_args()

        print args

        result = DepartHelper.create_depart(args['depart_name'], args['depart_type'], args['depart_desc'])
        if result:
            return DepartHelper.get_by_id(result)
        else:
            abort(400)

    @marshal_with(depart_fields)
    def put(self, depart_id):
        parser = reqparse.RequestParser()
        parser.add_argument('depart_name', dest='name', required=False)
        parser.add_argument('depart_type', dest='type', required=False)
        parser.add_argument('depart_desc', dest='description', required=False)
        args = parser.parse_args()

        fields = filter(lambda x: x[1] is not None, args.iteritems())
        print fields

        if not DepartHelper.modify(depart_id, fields):
            abort(400)
        
        return DepartHelper.get_by_id(depart_id)

    def delete(self, depart_id):
        if DepartHelper.delete_by_id(depart_id):
            return ''
        else:
            abort(400)