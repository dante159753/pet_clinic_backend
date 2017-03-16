# -*- coding: utf-8 -*-

from flask import Blueprint, request, g, url_for
from functools import wraps
import json

def check_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token', '')
        if len(token) < 6:
        	return json.dumps({'status': 'require token'}), 401

        return f(token, *args, **kwargs)
    return decorated_function

def require_service(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        flag = r_conn.get('manager:is.enabled')
        if not flag or flag == 'False':
            return json.dumps(
                {'status': 'service not on'}
            )

        return f(*args, **kwargs)
    return decorated_function

def format_by_formater(formater, multi=False):
    def real_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            result = f(*args, **kwargs)
            if multi:
                return map(lambda x: formater(x), result)
            else:
                return formater(result)
        return decorated_function
    return real_decorator

