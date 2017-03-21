# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.department import DepartHelper

depart_fields = {
    'depart_id': fields.Integer,
    'depart_name': fields.String,
    'depart_type': fields.Integer,
    'depart_desc': fields.String
}