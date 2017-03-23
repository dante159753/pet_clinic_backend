# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def video_formatter(t):
    return {
        'video_id': t[0],
        'video_name': t[1],
        'video_address': t[2],
        'screenshot': t[3]
    }

class VideoHelper:
    @staticmethod
    @format_by_formater(video_formatter)
    def get_by_id(video_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, address, screenshot from video where id=%s', 
            [video_id]
            )
        return cursor.fetchone()