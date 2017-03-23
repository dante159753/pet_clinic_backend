# -*- coding: utf-8 -*-

from backend import mysql, app
from backend.util import format_by_formater
import os

PIC_EXTS = ['jpg', 'jpeg', 'gif', 'bmp', 'png']

def picture_formatter(t):
    return {
        'picture_id': t[0],
        'picture_name': t[1],
        'picture_address': os.path.join('data', t[2]),
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

    @staticmethod
    @format_by_formater(picture_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, address, thumbnail from picture'
            )
        return cursor.fetchall()

    @staticmethod
    def create(pic_name, file):
        fname = file.filename
        address = os.path.join('picture', filename)
        if '.' in fname and fname.rsplit('.', 1)[1].lower() in PIC_EXTS:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], address))
        else:
            return False, 'invalid extension'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into picture (name, address) "
            "values (%s, %s)", 
            (pic_name, address)
            )
        db.commit()
        if cursor.rowcount != 1:
            return False, 'insert into db failed'

        return True, cursor.lastrowid