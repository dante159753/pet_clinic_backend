# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater
from .video import VideoHelper
from .picture import PictureHelper
from .department import DepartHelper

def roleplay_info_formatter(t):
    return {
        'role_id': t[0],
        'role_name': t[1],
        'role_desc': t[2],
        'page_size': t[3],
        'depart_id': t[4],
        'picture': t[5]
    }

def roleplay_page_formatter(t):
    return {
        'role_info': RoleplayInfoHelper.get_by_id(t[0]),
        'page_info': RoleplayPageInfoHelper.get_by_pagination(t[0], t[1]),
        'page_content': RoleplayContentHelper.get_by_page_id(t[2])
    }

def roleplay_page_info_formatter(t):
    return {
        'page_id': t[0],
        'page_title': t[1],
        'pagination': t[2],
    }

def roleplay_content_formatter(t):
    return {
        'content_id': t[0],
        'content_type': t[1],
        'text_content': t[2],
        'picture_content': PictureHelper.get_by_id(t[3]) if t[3] else None,
        'video_content': VideoHelper.get_by_id(t[4]) if t[4] else None
    }

class RoleplayInfoHelper:
    @staticmethod
    @format_by_formater(roleplay_info_formatter)
    def get_by_id(role_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, description, page_size, depart_id, picture from role where id=%s', 
            [role_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(roleplay_info_formatter)
    def get_by_name(role_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, description, page_size, depart_id, picture from role where name=%s', 
            [role_name]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(roleplay_info_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, name, description, page_size, depart_id, picture from role')
        return cursor.fetchall()

    @staticmethod
    def create_roleplay_info(role_name, role_desc, depart_id, picture_id):
        if RoleplayInfoHelper.get_by_name(role_name) is not None:
            return False, 'duplicate role play name'

        #if not PictureHelper.get_by_id(picture_id):
        #    return False, 'invalid picture_id'

        #if not DepartHelper.get_by_id(depart_id):
        #    return False, 'invalid depart_id'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into role (name, description, page_size, depart_id, picture) "
            "values (%s, %s, '0', %s, %s)", 
            (role_name, role_desc, depart_id, picture_id)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False, 'insert into db failed'
        else:
            return True, cursor.lastrowid

    @staticmethod
    def modify(role_id, fields):
        if RoleplayInfoHelper.get_by_id(role_id) is None:
            return False, 'can not find role_id'

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}=%s".format(k) for (k, v) in fields]
            )
        print set_sql

        arg_list = [v for (k, v) in fields]
        arg_list.append(role_id)
        print arg_list
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update role set {} where id=%s".format(set_sql),
            arg_list
            )
        db.commit()
        return True, None

    @staticmethod
    def delete_by_id(role_id):
        # TODO: delete all sub infos
        if RoleplayInfoHelper.get_by_id(role_id) is None:
            return False, 'can not find role_id'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from item_info where id=%s", 
            (role_id,)
            )
        db.commit()
        return cursor.rowcount == 1, None


class RoleplayPageInfoHelper:
    @staticmethod
    @format_by_formater(roleplay_page_info_formatter)
    def get_by_pagination(role_id, pagination):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, title, pagination from role_page where role_id=%s and pagination=%s', 
            [role_id, pagination]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(roleplay_page_info_formatter)
    def get_by_id(page_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, title, pagination from role_page where id=%s', 
            [page_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(roleplay_page_info_formatter, True)
    def get_by_roleid(role_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, title, pagination from role_page where role_id=%s', 
            [role_id]
            )
        return cursor.fetchall()

    @staticmethod
    def create_page_info(role_id, page_title, contents):
        if not RoleplayInfoHelper.get_by_id(role_id):
            return False, 'invalid role_id'
            
        db = mysql.get_db()
        cursor = db.cursor()

        # get page size
        cursor.execute(
            'select count(*) from role_page where role_id=%s', 
            (role_id,)
            )
        page_size = cursor.fetchone()[0]
        print page_size
        # insert role_page
        cursor.execute(
            "insert into role_page (role_id, title, pagination) "
            "values (%s, %s, %s)", 
            (role_id, page_title, int(page_size) + 1)
            )
        db.commit()
        page_id = cursor.lastrowid
        for content in contents:
            RoleplayContentHelper.create_content(page_id, content)

        return True, page_id

    @staticmethod
    def modify(role_id, pagination, page_title, contents):
        if RoleplayPageInfoHelper.get_by_pagination(role_id, pagination) is None:
            return False, 'can not find page'

        page = RoleplayPageInfoHelper.get_by_pagination(role_id, pagination)
        RoleplayContentHelper.delete_by_page_id(page['page_id'])
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update role_page set title=%s where id=%s",
            (page_title, page['page_id'])
            )
        db.commit()
        return True, None

    @staticmethod
    def delete(role_id, pagination):
        # TODO: delete all sub infos
        page = RoleplayPageInfoHelper.get_by_pagination(role_id, pagination)
        if page is None:
            return False, 'can not find page'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from role_page where role_id=%s and pagination=%s", 
            (role_id, pagination,)
            )
        cursor.execute(
            "delete from role_page_content where page_id=%s", 
            (page['page_id'],)
            )
        db.commit()
        return True, None


    @staticmethod
    def delete_by_role_id(role_id):
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from role_page where role_id=%s", 
            (role_id,)
            )
        for page_info in RoleplayPageInfoHelper.get_by_roleid(role_id):
            cursor.execute(
                "delete from role_page_content where page_id=%s", 
                (page_info['page_id'],)
                )
        db.commit()
        return True, None


class RoleplayPageHelper:
    @staticmethod
    @format_by_formater(roleplay_page_formatter)
    def get_by_pagination(role_id, pagination):
        return [role_id, pagination, RoleplayPageInfoHelper.get_by_pagination(role_id, pagination)['page_id']]


    @staticmethod
    @format_by_formater(roleplay_page_formatter)
    def get_by_id(role_id, page_id):
        return [role_id, RoleplayPageInfoHelper.get_by_id(page_id)['pagination'], page_id]


class RoleplayContentHelper:
    @staticmethod
    @format_by_formater(roleplay_content_formatter, True)
    def get_by_page_id(page_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, content_type, text_content, picture_id, video_id from role_page_content where page_id=%s', 
            [page_id]
            )
        return cursor.fetchall()

    @staticmethod
    def create_content(page_id, content):
        content_type = content['content_type']

        sql_content = None # 字段名
        arg_content = None # 内容
        if str(content_type) == '1':
            sql_content = 'text_content'
            arg_content = content['text_content']
        elif str(content_type) == '2':
            sql_content = 'video_id'
            arg_content = content['video_content']
        elif str(content_type) == '3':
            sql_content = 'picture_id'
            arg_content = content['picture_content']
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into role_page_content (page_id, content_type, {}) values (%s, %s, %s)".format(sql_content),
            (page_id, content_type, arg_content)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        return cursor.lastrowid


    @staticmethod
    def delete_by_id(content_id):
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from role_page_content where id=%s", 
            (content_id,)
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_page_id(page_id):
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from role_page_content where page_id=%s", 
            (page_id,)
            )
        db.commit()
        return True

