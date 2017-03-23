# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.case import CaseInfoHelper, CasePageHelper
from .picture import picture_fields
from .video import video_fields

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
    def get(self):
        result = CaseInfoHelper.get_all()
        if result is None:
            abort(404)
        return result

class Case(Resource):
    @marshal_with(case_fields)
    def get(self, case_id):
        result = CasePageHelper.get_by_id(case_id)
        if result is None:
            abort(404)
        return result

