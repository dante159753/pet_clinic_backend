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
        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        result = VideoHelper.create(args['file'])
        if result[0]:
            return VideoHelper.get_by_id(result[1])
        else:
            abort(400, result[1])

    def delete(self, video_id):
        if VideoHelper.delete(video_id):
            return ''
        else:
            abort(400)
