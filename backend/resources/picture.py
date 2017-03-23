# -*- coding: utf-8 -*-
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from backend.models.picture import PictureHelper
import werkzeug

picture_fields = {
    'picture_id': fields.Integer,
    'picture_name': fields.String,
    'picture_address': fields.String,
    'thumbnail': fields.String
}

class Picture(Resource):
    @marshal_with(picture_fields)
    def get(self, pic_id=None):
        result = None
        if pic_id is not None:
            result = PictureHelper.get_by_id(pic_id)
        else:
            result = PictureHelper.get_all()
        if result is None:
            abort(404)
        return result

    @marshal_with(picture_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        result = PictureHelper.create(args['file'])
        if result[0]:
            return PictureHelper.get_by_id(result[1])
        else:
            abort(400, result[1])

    def delete(self, pic_id):
        if PictureHelper.delete_by_id(pic_id):
            return ''
        else:
            abort(400)