# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.case import CaseInfoHelper, CasePageHelper, CaseCategoryHelper, CaseContentHelper
from .picture import picture_fields
from .video import video_fields
import json

case_type_fields = {
    'case_type_id': fields.String,
    'case_type_name': fields.String,
    'case_type_desc': fields.String
}

case_info_fields = {
    'case_type': fields.Nested(case_type_fields),
    'case_id': fields.String,
    'case_name': fields.String,
    'case_desc': fields.String
}

case_content = {
    'case_content_id': fields.Integer,
    'case_content_type': fields.Integer,
    'text_content': fields.String,
    'picture_content': fields.Nested(picture_fields),
    'video_content': fields.Nested(video_fields)
}

case_category = {
    'category_id': fields.Integer,
    'category_name': fields.String,
    'category_desc': fields.String,
    'category_content': fields.List(fields.Nested(case_content))
}

case_fields = {
    'case_info': fields.Nested(case_info_fields),
    'categories': fields.List(fields.Nested(case_category))
}

class CaseInfo(Resource):
    @marshal_with(case_info_fields)
    def get(self, case_id=None):
        result = None
        if case_id:
            result = CaseInfoHelper.get_by_id(case_id)
        else:
            result = CaseInfoHelper.get_all()
        if result is None:
            print 'no case info'
            abort(404)
        return result

    @marshal_with(case_info_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('case_type_id', required=True, help='case_type_id is required')
        parser.add_argument('case_name', required=True, help='case_name is required')
        parser.add_argument('case_desc', required=True, help='case_desc is required')
        args = parser.parse_args()

        result = CaseInfoHelper.create_case_info(
            args['case_type_id'], 
            args['case_name'], 
            args['case_desc']
            )
        if not result[0]:
            abort(404)
        return CaseInfoHelper.get_by_id(result[1])

    @marshal_with(case_info_fields)
    def put(self, case_id):
        parser = reqparse.RequestParser()
        parser.add_argument('case_type_id', dest='type_id')
        parser.add_argument('case_name', dest='name')
        parser.add_argument('case_desc', dest='description')
        args = parser.parse_args()

        fields = filter(lambda x: x[1] is not None, args.iteritems())
        result = CaseInfoHelper.modify(case_id, fields)
        if not result[0]:
            abort(404)
        return CaseInfoHelper.get_by_id(case_id)

    @marshal_with(case_info_fields)
    def delete(self, case_id):
        parser = reqparse.RequestParser()
        parser.add_argument('case_type_id', required=True, help='case_type_id is required')
        parser.add_argument('case_name', required=True, help='case_name is required')
        parser.add_argument('case_desc', required=True, help='case_desc is required')
        args = parser.parse_args()

        result = CaseInfoHelper.create_case_info(
            args['case_type_id'], 
            args['case_name'], 
            args['case_desc']
            )
        if not result[0]:
            abort(404)
        return CaseInfoHelper.get_by_id(result[1])

class Case(Resource):
    @marshal_with(case_fields)
    def get(self, case_id):
        result = CasePageHelper.get_by_id(case_id)
        if result is None:
            abort(404)
        return result

    @marshal_with(case_fields)
    def put(self, case_id):
        parser = reqparse.RequestParser()
        parser.add_argument('categories', action='append', required=True, help='categories is required')
        args = parser.parse_args()

        if not CaseInfoHelper.get_by_id(case_id):
            abort(404)

        for str_category in args['categories']:
            try:
                category = json.loads(str_category)
                print category
                category_id = CaseCategoryHelper.create_case_category(
                    case_id, 
                    category['category_name'], 
                    category['category_desc']
                    )
                if not category_id:
                    print 'can not create category'
                for content in category['category_content']:
                    CaseContentHelper.create_case_content(
                        category_id, 
                        content['case_content_type'], 
                        content['text_content'],
                        content['picture_content'],
                        content['video_content']
                        )

            except ValueError, e:
                print e
                abort(400)
        
        return CasePageHelper.get_by_id(case_id)
