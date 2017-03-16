# -*- coding: utf-8 -*-
from flask_restful import Resource

class User(Resource):
    def get(self, user_id=None):
        return 'User: get'
    def post(self):
        return 'User: post'