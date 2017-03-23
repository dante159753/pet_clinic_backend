# -*- coding: utf-8 -*-
from flask import Blueprint, request, g, url_for
from flask_restful import abort, reqparse
from functools import wraps
import json
import jwt
from backend import app

def generate_token(obj):
    return jwt.encode(obj, app.config['JWT_SECRET'], algorithm='HS256')

def check_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token', '')
        try:
            obj = jwt.decode(token, app.config['JWT_SECRET'], algorithm='HS256')
            # check obj TODO
        	
        except jwt.InvalidTokenError:
            abort(401)

        return f(*args, **kwargs)
    return decorated_function

def format_by_formater(formater, multi=False):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            try:
                if multi:
                    return map(lambda x: formater(x), result)
                else:
                    return formater(result)
            except TypeError:
                return None
        return decorated_function
    return real_decorator

