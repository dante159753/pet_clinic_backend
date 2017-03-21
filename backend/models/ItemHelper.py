# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater

def item_formatter(t):
    return {
        'item_id': t[0],
        'item_name': t[1],
        'item_desc': t[2],
        'item_type': {
            'item_type_id': t[3],
            'item_type_name': t[4],
            'item_type_desc': t[5]
        }
    }

def item_type_formatter(t):
    return {
        'item_type_id': t[3],
        'item_type_name': t[4],
        'item_type_desc': t[5]
    }


class ItemTypeHelper:
    @staticmethod
    @format_by_formater(item_type_formatter)
    def get_by_id(item_type_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select item_type.id, item_type.name, item_type.description'
            ' from item_type'
            ' where item_type.id=%s', 
            [item_type_id]
            )
        return cursor.fetchone()

class ItemHelper:
    @staticmethod
    @format_by_formater(item_formatter, True)
    def get_by_depart_id(depart_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select item.id, item.name, item.description, item.type_id, '
            'item_type.name, item_type.description'
            ' from item, item_type, depart_item'
            ' where depart_item.item_type = item_type.id and depart_item.item_id = item.id'
            '  and depart_item.depart_id=%s', 
            [depart_id]
            )
        return cursor.fetchall()

    @staticmethod
    def filter_by_item_type(item_list, item_type_id):
        return filter(lambda item: item['item_type']['item_type_id'] == item_type_id, item_list)

    @staticmethod
    @format_by_formater(item_formatter)
    def get_by_item_id(item_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select item.id, item.name, item.description, item.type_id, '
            'item_type.name, item_type.description'
            ' from item, item_type'
            ' where item.type_id = item_type.id'
            '  and item.id=%s', 
            [item_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(item_formatter)
    def get_by_item_name(depart_id, item_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select item.id, item.name, item.description, item.type_id, '
            'item_type.name, item_type.description'
            ' from item, item_type, depart_item'
            ' where depart_item.item_type = item_type.id and depart_item.item_id = item.id'
            '  and depart_item.depart_id=%s and item.name=%s', 
            [depart_id, item_name]
            )
        return cursor.fetchone()

    @staticmethod
    def create_item(depart_id, item_type_id, item_name, item_desc):
        if ItemHelper.get_by_item_name(depart_id, item_name) is not None:
            print 'duplicated item name'
            return False
        if ItemTypeHelper.get_by_id(item_type_id) is None:
            print 'can not find item type'
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into item (name, type_id, description) "
            "values (%s, %s, %s)", 
            (item_name, item_type_id, item_desc)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            print 'insert item failed'
            return False
        item_id = cursor.lastrowid
        if not ItemHelper.add_depart_item(depart_id, item_id, item_type_id):
            print 'add depart_item failed'
            return False

        return True

    @staticmethod
    def add_depart_item(depart_id, item_id, item_type_id):
        if ItemTypeHelper.get_by_id(item_type_id) is None:
            print 'can not find item type'
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into depart_item (depart_id, item_id, item_type) "
            "values (%s, %s, %s)", 
            (depart_id, item_id, item_type_id)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def modify(depart_id, item_id, fields):
        if ItemHelper.get_by_item_id(depart_id, item_id) is None:
            return False

        set_sql = reduce((lambda s1, s2: s1 +',' + s2), ["{}='{}'".format(k, v) for (k, v) in fields])
        print set_sql
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update item set {} where id in ".format(set_sql),
            (,)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(depart_id):
        if ItemHelper.get_by_id(depart_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from department where id=%s", 
            (depart_id,)
            )
        db.commit()
        return cursor.rowcount == 1

