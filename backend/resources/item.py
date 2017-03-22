# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.item import ItemHelper, ItemTypeHelper

item_type_fields = {
    'item_type_id': fields.Integer,
    'item_type_name': fields.String,
    'item_type_desc': fields.String
}

item_fields = {
    'item_id': fields.Integer,
    'item_type': fields.Nested(item_type_fields),
    'item_name': fields.String,
    'item_desc': fields.String
}

class Item(Resource):
    @marshal_with(item_fields)
    def get(self, depart_id, item_id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('item_type_id', type=int, required=False)
        args = parser.parse_args()

        print args

        result = None
        if item_id:
            result = ItemHelper.get_by_item_id(item_id)
        else:
            result = ItemHelper.get_by_depart_id(depart_id)

        if result is None:
            abort(404)

        if args['item_type_id'] and item_id is None:
            result = ItemHelper.filter_by_item_type(result, args['item_type_id'])
        return result

    @marshal_with(item_fields)
    def post(self, depart_id):
        parser = reqparse.RequestParser()
        parser.add_argument('depart_id', required=True, help='depart_id is required')
        parser.add_argument('item_type_id', required=True, help='item_type_id is required')
        parser.add_argument('item_name', required=True, help='item_name is required')
        parser.add_argument('item_desc', required=True, help='item_desc is required')
        args = parser.parse_args()

        if ItemHelper.create_item(args['depart_id'], args['item_type_id'], args['item_name'], args['item_desc']):
            return ItemHelper.get_by_item_name(args['depart_id'], args['item_name'])
        else:
            abort(400)

    @marshal_with(item_fields)
    def put(self, depart_id, item_id):
        parser = reqparse.RequestParser()
        parser.add_argument('item_type_id', dest='type_id', required=False)
        parser.add_argument('item_name', dest='name', required=False)
        parser.add_argument('item_desc', dest='description', required=False)
        args = parser.parse_args()

        print args
        fields = filter(lambda x: x[1] is not None, args.iteritems())

        if not ItemHelper.modify(item_id, fields):
            abort(400)
        
        return ItemHelper.get_by_item_id(item_id)

    def delete(self, depart_id, item_id):
        if ItemHelper.delete_by_id(item_id):
            return ''
        else:
            abort(400)

    def options(self, depart_id, item_id=None):
        return '', 200, { 
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Methods' : 'PUT,GET,POST,DELETE'
            }


class ItemType(Resource):
    @marshal_with(item_type_fields)
    def get(self, item_type_id=None):

        result = None
        if item_type_id:
            result = ItemTypeHelper.get_by_id(item_type_id)
        else:
            result = ItemTypeHelper.get_all()

        if result is None:
            abort(404)

        return result

    @marshal_with(item_type_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_type_name', required=True, help='item_type_name is required')
        parser.add_argument('item_type_desc', required=True, help='item_type_desc is required')
        args = parser.parse_args()

        if ItemTypeHelper.create_item_type(args['item_type_name'], args['item_type_desc']):
            return ItemTypeHelper.get_by_name(args['item_type_name'])
        else:
            abort(400)

    @marshal_with(item_type_fields)
    def put(self, item_type_id):
        parser = reqparse.RequestParser()
        parser.add_argument('item_type_name', dest='name', required=False)
        parser.add_argument('item_type_desc', dest='description', required=False)
        args = parser.parse_args()

        print args
        fields = filter(lambda x: x[1] is not None, args.iteritems())

        if not ItemTypeHelper.modify(item_type_id, fields):
            abort(400)
        
        return ItemTypeHelper.get_by_id(item_type_id)

    def delete(self, item_type_id):
        if ItemTypeHelper.delete_by_id(item_type_id):
            return ''
        else:
            abort(400)

    def options(self, item_type_id=None):
        return '', 200, { 
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Methods' : 'PUT,GET,POST,DELETE'
            }