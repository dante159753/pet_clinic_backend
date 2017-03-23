# -*- coding: utf-8 -*-

from backend import mysql, app
from backend.util import format_by_formater
import os
import uuid

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
    def create(file):
        pic_name = file.filename
        ext = pic_name.rsplit('.', 1)[1].lower()
        if '.' in pic_name and ext in PIC_EXTS:
            new_fname = str(uuid.uuid4()) + '.' + ext
            address = os.path.join('picture', new_fname)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], address))
            
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
        else:
            return False, 'invalid extension'

    @staticmethod
    def delete(picture_id):
        picture = PictureHelper.get_by_id(picture_id)
        if not picture:
            return False, 'can not find picture id'

        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from picture "
            "where id=%s", 
            (picture_id,)
            )
        db.commit()
        if cursor.rowcount != 1:
            return False, 'insert into db failed'
        else:
            actual_address = picture['picture_address'].split('/', 1)[1]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], actual_address))
            return True, None