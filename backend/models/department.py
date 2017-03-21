# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def depart_formatter(t):
    return {
        'depart_id': t[0],
        'depart_name': t[1],
        'depart_type': t[2],
        'depart_desc': t[3]
    }

class DepartHelper:
    @staticmethod
    @format_by_formater(depart_formatter)
    def get_by_id(depart_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, type, description from department where id=%s', 
            [depart_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(depart_formatter)
    def get_by_name(depart_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, type, description from department where name=%s', 
            [depart_name]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(depart_formatter, True)
    def get_by_worker(worker_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select department.id, department.name, department.type, department.description '
            'from department, depart_worker '
            'where department.id = depart_worker.depart_id and depart_worker.worker_id=%s', 
            (worker_id,)
            )
        return cursor.fetchall()

    @staticmethod
    @format_by_formater(depart_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, name, type, description from department')
        return cursor.fetchall()

    @staticmethod
    def create_depart(depart_name, depart_type, depart_desc):
        if DepartHelper.get_by_name(depart_name) is not None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into department (name, type, description) "
            "values (%s, %s, %s)", 
            (depart_name, depart_type, depart_desc)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify(depart_id, fields):
        if DepartHelper.get_by_id(depart_id) is None:
            return False

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}='{}'".format(k, v) for (k, v) in fields]
            )
        print set_sql
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update department set {} where id=%s".format(set_sql),
            (depart_id,)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(depart_id):
        if DepartHelper.get_by_id(depart_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from department where id=%s", 
            (depart_id,)
            )
        db.commit()
        return cursor.rowcount == 1

