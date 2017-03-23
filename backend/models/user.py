# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def user_formater(user_tuple):
    return {
        'user_id': user_tuple[0],
        'user_name': user_tuple[1]
    }

class UserHelper:
    @staticmethod
    @format_by_formater(user_formater)
    def get_by_id(user_id):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from user_account where id=%s', [user_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(user_formater)
    def get_by_name(user_name):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from user_account where username=%s', (user_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(user_formater, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from user_account')
        return cursor.fetchall()

    @staticmethod
    def create_user(username, password):
        if UserHelper.get_by_name(username) is not None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into user_account (username, password) "
            "values (%s, %s)", 
            (username, password)
            )
        db.commit()
        # row count为1表示插入成功
        return cursor.rowcount == 1

    @staticmethod
    def modify_username(user_id, username):
        if UserHelper.get_by_id(user_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update user_account set username=%s where id=%s", 
            (username, user_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(user_id, password):
        if UserHelper.get_by_id(user_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update user_account set password=%s where id=%s", 
            (password, user_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def check_password(username, password):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select count(*) from user_account where username=%s and password=%s', 
            (username, password)
            )
        return cursor.fetchone()[0] == 1

    @staticmethod
    def delete_by_id(user_id):
        if UserHelper.get_by_id(user_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from user_account where id=%s", 
            (user_id,)
            )
        db.commit()
        return cursor.rowcount == 1

