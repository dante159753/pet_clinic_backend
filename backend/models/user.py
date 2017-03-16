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
    def check_password(user_name, password):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select count(*) from user_account where username=%s and password=%s', 
            (user_name, password)
            )
        return cursor.rowcount == 1


