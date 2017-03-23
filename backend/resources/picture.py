# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse

picture_fields = {
    'picture_id': fields.Integer,
    'picture_name': fields.String,
    'picture_address': fields.String,
    'thumbnail': fields.String
}