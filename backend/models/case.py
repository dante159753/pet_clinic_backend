# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater
from .video import VideoHelper
from .picture import PictureHelper

def case_type_formatter(t):
    return {
        'case_type_id': t[0],
        'case_type_name': t[1],
        'case_type_desc': t[2]
    }

def case_info_formatter(t):
    return {
        'case_id': t[0],
        'case_type': CaseTypeHelper.get_by_id(t[1]),
        'case_name': t[2],
        'case_desc': t[3]
    }

def case_page_formatter(t):
    return {
        'case_info': CaseInfoHelper.get_by_id(t[0]),
        'categories': CaseCategoryHelper.get_by_case_id(t[0])
    }


def case_category_formatter(t):
    return {
        'category_id': t[0],
        'category_name': t[1],
        'category_desc': t[2],
        'category_content': CaseContentHelper.get_by_category(t[0])
    }

def case_content_formatter(t):
    return {
        'case_content_id': t[0],
        'case_content_type': t[1],
        'text_content': t[2],
        'picture_content': PictureHelper.get_by_id(t[3]) if t[3] else None,
        'video_content': VideoHelper.get_by_id(t[4]) if t[4] else None
    }

class CaseTypeHelper:
    @staticmethod
    @format_by_formater(case_type_formatter)
    def get_by_id(case_type_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, description from case_type where id=%s', 
            [case_type_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_type_formatter)
    def get_by_name(case_type_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, description from case_type where name=%s', 
            [case_type_name]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_type_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, name, description from case_type')
        return cursor.fetchall()

    @staticmethod
    def create_case_type(case_type_name, case_type_desc):
        if CaseTypeHelper.get_by_name(case_type_name) is not None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into case_type (name, description) "
            "values (%s, %s)", 
            (case_type_name, case_type_desc)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return cursor.lastrowid

    @staticmethod
    def modify(case_type_id, fields):
        if CaseTypeHelper.get_by_id(case_type_id) is None:
            return False

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}=%s".format(k) for (k, v) in fields]
            )
        print set_sql

        arg_list = [v for (k, v) in fields]
        arg_list.append(case_type_id)
        print arg_list
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update case_type set {} where id=%s".format(set_sql),
            arg_list
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(case_type_id):
        if CaseTypeHelper.get_by_id(case_type_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from case_type where id=%s", 
            (case_type_id,)
            )
        db.commit()
        return cursor.rowcount == 1

class CaseInfoHelper:
    @staticmethod
    @format_by_formater(case_info_formatter)
    def get_by_id(case_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, type_id, name, description from case_info where id=%s', 
            [case_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_info_formatter)
    def get_by_name(case_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, type_id, name, description from case_info where name=%s', 
            [case_name]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_info_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, type_id, name, description from case_info')
        return cursor.fetchall()

    @staticmethod
    def filter_by_case_type(case_list, case_type_id):
        return filter(lambda case: int(case['case_type']['case_type_id']) == int(case_type_id), case_list)

    @staticmethod
    def create_case_info(case_type_id, case_name, case_desc):
        if CaseInfoHelper.get_by_name(case_name) is not None:
            return False, 'duplicate case name'

        if CaseTypeHelper.get_by_id(case_type_id) is None:
            return False, 'can not find case type'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into case_info (type_id, name, description) "
            "values (%s, %s, %s)", 
            (case_type_id, case_name, case_desc)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False, 'insert into db failed'
        else:
            return True, cursor.lastrowid

    @staticmethod
    def modify(case_id, fields):
        if CaseInfoHelper.get_by_id(case_id) is None:
            return False, 'can not find case_id'

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}=%s".format(k) for (k, v) in fields]
            )
        print set_sql

        arg_list = [v for (k, v) in fields]
        arg_list.append(case_id)
        print arg_list
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update case_info set {} where id=%s".format(set_sql),
            arg_list
            )
        db.commit()
        return cursor.rowcount == 1, None

    @staticmethod
    def delete_by_id(case_id):
        if CaseInfoHelper.get_by_id(case_id) is None:
            return False, 'can not find case_id'
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from case_info where id=%s", 
            (case_id,)
            )
        cursor.execute(
            "delete from case_info_category where case_id=%s", 
            (case_id,)
            )
        db.commit()

        result = CaseCategoryHelper.delete_by_case(case_id)[0]:
        if not result[0]:
            return result;


class CasePageHelper:
    @staticmethod
    @format_by_formater(case_page_formatter)
    def get_by_id(case_id):
        return [case_id]


class CaseCategoryHelper:
    @staticmethod
    @format_by_formater(case_category_formatter)
    def get_by_id(category_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, name, description from case_category where id=%s', 
            [category_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_category_formatter, True)
    def get_by_case_id(case_id):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, name, description from case_category where '
            'id in (select category_id from case_info_category where case_id=%s)',
            (case_id,)
            )
        return cursor.fetchall()

    @staticmethod
    def create_case_category(case_id, category_name, category_desc):
        if CaseInfoHelper.get_by_id(case_id) is None:
            print 'can not find case'
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into case_category (name, description) "
            "values (%s, %s)", 
            (category_name, category_desc)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        
        category_id = cursor.lastrowid
        cursor.execute(
            "insert into case_info_category (case_id, category_id) "
            "values (%s, %s)", 
            (case_id, category_id)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return category_id


    @staticmethod
    def modify(category_id, fields):
        if CaseCategoryHelper.get_by_id(category_id) is None:
            return False

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}=%s".format(k) for (k, v) in fields]
            )
        print set_sql

        arg_list = [v for (k, v) in fields]
        arg_list.append(category_id)
        print arg_list
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update case_category set {} where id=%s".format(set_sql),
            arg_list
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(category_id):
        if CaseCategoryHelper.get_by_id(category_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from case_category where id=%s", 
            (category_id,)
            )
        cursor.execute(
            "delete from case_category_content where category_id=%s", 
            (category_id,)
            )
        db.commit()
        return True

    @staticmethod
    def delete_by_case(case_id):
        for category in CaseCategoryHelper.get_by_case_id(case_id):
            for content in category['category_content']:
                if not CaseContentHelper.delete_by_id(contnet['case_content_id']):
                    return False, 'can not delete content'
            if not CaseCategoryHelper.delete_by_id(category['cate_category_id']):
                return False, 'can not delete category'
        return True, None


class CaseContentHelper:
    @staticmethod
    @format_by_formater(case_content_formatter)
    def get_by_id(content_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select id, content_type, text_content, picture_id, video_id from case_content where id=%s', 
            [content_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(case_content_formatter, True)
    def get_by_category(category_id):
        cursor = mysql.get_db().cursor()
        cursor.execute('select id, content_type, text_content, picture_id, video_id from case_content where '
            'id in (select content_id from case_category_content where category_id=%s)',
            (category_id,)
            )
        return cursor.fetchall()

    @staticmethod
    def create_case_content(category_id, content_type, text, picture, video):
        if CaseCategoryHelper.get_by_id(category_id) is None:
            print 'can not find cate category'
            return False

        sql_content = None # 字段名
        arg_content = None # 内容
        if str(content_type) == '1':
            sql_content = 'text_content'
            arg_content = text
        elif str(content_type) == '2':
            sql_content = 'video_id'
            arg_content = video
        elif str(content_type) == '3':
            sql_content = 'picture_id'
            arg_content = picture
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into case_content (content_type, {}) values (%s, %s)".format(sql_content),
            (content_type, arg_content)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        
        content_id = cursor.lastrowid
        cursor.execute(
            "insert into case_category_content (category_id, content_id) "
            "values (%s, %s)", 
            (category_id, content_id)
            )
        db.commit()
        # row count为1表示插入成功
        if cursor.rowcount != 1:
            return False
        else:
            return content_id


    @staticmethod
    def delete_by_id(content_id):
        if CaseContentHelper.get_by_id(content_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from case_content where id=%s", 
            (category_id,)
            )
        db.commit()
        return cursor.rowcount == 1

