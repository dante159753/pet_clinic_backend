# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse

video_fields = {
    'video_id': fields.Integer,
    'video_name': fields.String,
    'video_address': fields.String,
    'screenshot': fields.String
}