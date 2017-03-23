# -*- coding: utf-8 -*-

from backend import mysql, app
from backend.util import format_by_formater
import os
import uuid

VIDEO_EXTS = ['mp4', 'wmv', 'wav', 'mpeg', 'mov', 'flv', 'avi']

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

    @staticmethod
    @format_by_formater(video_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, address, screenshot from video'
            )
        return cursor.fetchall()

    @staticmethod
    def create(file):
        video_name = file.filename
        ext = video_name.rsplit('.', 1)[1].lower()
        if '.' in video_name and ext in VIDEO_EXTS:
            new_fname = str(uuid.uuid4()) + '.' + ext
            address = os.path.join('video', new_fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], address))
            
            db = mysql.get_db()
            cursor = db.cursor()
            cursor.execute(
                "insert into video (name, address) "
                "values (%s, %s)", 
                (video_name, address)
                )
            db.commit()
            if cursor.rowcount != 1:
                return False, 'insert into db failed'
    
            return True, cursor.lastrowid
        else:
            return False, 'invalid extension'

    @staticmethod
    def delete(video_id):
        video = VideoHelper.get_by_id(video_id)
        if not video:
            return False, 'can not find video id'

        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from video "
            "where id=%s", 
            (video_id,)
            )
        db.commit()
        if cursor.rowcount != 1:
            return False, 'insert into db failed'
        else:
            actual_address = video['video_address'].split('/', 1)[1]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], actual_address))
            return True, None