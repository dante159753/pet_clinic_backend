# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.video import VideoHelper

video_fields = {
    'video_id': fields.Integer,
    'video_name': fields.String,
    'video_address': fields.String,
    'screenshot': fields.String
}

class Video(Resource):
    @marshal_with(video_fields)
    def get(self, video_id=None):
        result = None
        if video_id is not None:
            result = VideoHelper.get_by_id(video_id)
        else:
            result = VideoHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(video_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='username is required')
        parser.add_argument('password', required=True, help='password is required')
        args = parser.parse_args()

        if VideoHelper.create_user(args['username'], args['password']):
            return VideoHelper.get_by_name(args['username'])
        else:
            abort(400)

    def delete(self, video_id):
        if VideoHelper.delete_by_id(video_id):
            return ''
        else:
            abort(400)

    def options(self, video_id=None):
        return '', 200, { 
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Methods' : 'PUT,GET,POST,DELETE',
            'Access-Control-Allow-Headers': 'token'
            }
