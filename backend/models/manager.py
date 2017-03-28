# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def authority_formatter(authority_tuple):
    return {
        'authority_id': authority_tuple[0],
        'authority_desc': authority_tuple[1]
    }

def manager_formatter(manager_tuple):
    return {
        'manager_id': manager_tuple[0],
        'manager_name': manager_tuple[1]
    }


class AuthorityHelper:
    @staticmethod
    @format_by_formater(authority_formatter)
    def get_by_auth_id(auth_id):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, description from authority where id=%s', [auth_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(authority_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, description from authority')
        return cursor.fetchall()

    @staticmethod
    @format_by_formater(authority_formatter, True)
    def get_by_manager_id(manager_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select auth.id, auth.description from authority auth, manager_auth '
            'where manager_auth.manager_id=%s and auth.id = manager_auth.auth_id', 
            [manager_id]
            )
        return cursor.fetchall()

    @staticmethod
    def add_authority(manager_id, auth_id):
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into manager_auth(manager_id, auth_id) "
            "values(%s, %s)", 
            (manager_id, auth_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def remove_authority(manager_id, auth_id):
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from manager_auth "
            "where manager_id=%s and auth_id=%s", 
            (manager_id, auth_id)
            )
        db.commit()
        return cursor.rowcount == 1


class ManagerHelper:
    @staticmethod
    @format_by_formater(manager_formatter)
    def get_by_id(manager_id):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from manager_account where id=%s', [manager_id])
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(manager_formatter)
    def get_by_name(manager_name):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from manager_account where username=%s', (manager_name,))
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(manager_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, username from manager_account')
        return cursor.fetchall()

    @staticmethod
    def create_manager(username, password, auth_list=None):
        if ManagerHelper.get_by_name(username) is not None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into manager_account (username, password) "
            "values (%s, %s)", 
            (username, password)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            if auth_list:
                # get created manager
                manager = ManagerHelper.get_by_name(username)
                # success, insert authorities
                is_success = True
                for auth_id in auth_list:
                    if AuthorityHelper.get_by_id(auth_id) is not None:
                        if not AuthorityHelper.add_authority(manager['manager_id'], auth_id):
                            is_success = False
                        else:
                            pass
                    else:
                        pass
    
                return is_success
            else:
                return True

    @staticmethod
    def modify_username(manager_id, manager_name):
        if ManagerHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update manager_account set username=%s where id=%s", 
            (manager_name, manager_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def modify_password(manager_id, password):
        if UserHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update manager_account set password=%s where id=%s", 
            (password, manager_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def check_password(manager_name, password):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select count(*) from manager_account where username=%s and password=%s', 
            (manager_name, password)
            )
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(manager_id):
        if UserHelper.get_by_id(manager_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from manager_account where id=%s", 
            (manager_id,)
            )
        db.commit()
        return cursor.rowcount == 1

