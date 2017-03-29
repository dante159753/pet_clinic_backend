# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.roleplay import RoleplayInfoHelper, RoleplayPageInfoHelper, RoleplayPageHelper, RoleplayContentHelper
from .picture import picture_fields
from .video import video_fields
import json

roleplay_info_fields = {
    'role_id': fields.Integer,
    'role_name': fields.String,
    'role_desc': fields.String,
    'page_size': fields.Integer,
    'depart_id': fields.String,
    'picture': fields.String,
}

page_content = {
    'content_id': fields.Integer,
    'content_type': fields.Integer,
    'text_content': fields.String,
    'picture_content': fields.Nested(picture_fields),
    'video_content': fields.Nested(video_fields)
}

page_info_fields = {
    'page_id': fields.Integer,
    'pagination': fields.Integer,
    'page_title': fields.String
}

roleplay_page_fields = {
    'role_info': fields.Nested(roleplay_info_fields),
    'page_info': fields.Nested(page_info_fields),
    'page_content': fields.List(fields.Nested(page_content))
}

class RoleplayInfo(Resource):
    @marshal_with(roleplay_info_fields)
    def get(self, role_id=None):
        if not role_id:
            result = RoleplayInfoHelper.get_all()
        else:
            result = RoleplayInfoHelper.get_by_id(role_id)
        if result is None:
            print 'no role play info'
            abort(404)
        return result

    @marshal_with(roleplay_info_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', required=True, help='role_name is required')
        parser.add_argument('role_desc', required=True, help='role_desc is required')
        parser.add_argument('depart_id', required=True, help='depart_id is required')
        parser.add_argument('picture_id', required=True, help='picture_id is required')
        args = parser.parse_args()

        result = RoleplayInfoHelper.create_roleplay_info(
            args['role_name'], 
            args['role_desc'], 
            args['depart_id'],
            args['picture_id'],
            )
        if not result[0]:
            print result
            abort(400)
        return RoleplayInfoHelper.get_by_id(result[1])


class RoleplayPageInfo(Resource):
    @marshal_with(page_info_fields)
    def get(self, role_id):
        result = RoleplayPageInfoHelper.get_by_roleid(role_id)
        if result is None:
            print 'no role play info'
            abort(404)
        return result

    @marshal_with(roleplay_info_fields)
    def put(self, role_id):
        parser = reqparse.RequestParser()
        parser.add_argument('role_name', dest='name')
        parser.add_argument('role_desc', dest='description')
        parser.add_argument('depart_id', dest='depart_id')
        parser.add_argument('picture_id', dest='picture')
        args = parser.parse_args()
        print args

        # remove previous pages
        RoleplayPageInfoHelper.delete_by_role_id(role_id)
        args['page_size'] = 0

        fields = filter(lambda x: x[1] is not None, args.iteritems())
        result = RoleplayInfoHelper.modify(role_id, fields)
        if not result[0]:
            print result[1]
            abort(500)
        return RoleplayInfoHelper.get_by_id(role_id)

    @marshal_with(roleplay_info_fields)
    def delete(self, role_id):

        result = RoleplayInfoHelper.delete_by_id(role_id)
        if not result[0]:
            abort(404)
        return ''

class RoleplayPage(Resource):
    @marshal_with(roleplay_page_fields)
    def get(self, role_id, pagination):
        result = RoleplayPageHelper.get_by_pagination(role_id, pagination)
        if result is None:
            abort(404)
        return result

    @marshal_with(page_info_fields)
    def post(self, role_id):
        parser = reqparse.RequestParser()
        parser.add_argument('roleplay_page', required=True, help='roleplay_page is required')
        args = parser.parse_args()

        page = json.loads(args['roleplay_page'])
        result = RoleplayPageInfoHelper.create_page_info(
            role_id, 
            page['page_info']['page_title'], 
            page['page_content']
            )
        if not result[0]:
            abort(404)
        return RoleplayPageInfoHelper.get_by_id(result[1])

    @marshal_with(page_info_fields)
    def put(self, role_id, pagination):
        parser = reqparse.RequestParser()
        parser.add_argument('roleplay_page', required=True, help='roleplay_page is required')
        args = parser.parse_args()

        if not RoleplayPageInfoHelper.get_by_pagination(role_id, pagination):
            abort(404)

        page = json.loads(args['roleplay_page'])
        result = RoleplayPageInfoHelper.modify(
            role_id, 
            pagination,
            page['page_info']['page_title'], 
            page['page_content']
            )
        if not result[0]:
            abort(500)
        return RoleplayPageHelper.get_by_pagination(role_id, pagination)

    def delete(self, role_id):
        # TODO: add delete logical
        result = RoleplayPageInfoHelper.delete_by_role_id(role_id)
        if not result[0]:
            abort(500)
        return ''
