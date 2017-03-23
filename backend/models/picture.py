# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def picture_formatter(t):
    return {
        'picture_id': t[0],
        'picture_name': t[1],
        'picture_address': t[2],
        'thumbnail': t[3]
    }

class PictureHelper:
    @staticmethod
    @format_by_formater(picture_formatter)
    def get_by_id(picture_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, address, thumbnail from picture where id=%s', 
            [picture_id]
            )
        return cursor.fetchone()