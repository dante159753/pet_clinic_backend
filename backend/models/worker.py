# -*- coding: utf-8 -*-

from backend import mysql
from backend.util import format_by_formater
from backend.models.department import DepartHelper

def worker_formatter(t):
    return {
        'worker_id': t[0],
        'worker_name': t[1],
        'departments': DepartHelper.get_by_worker(t[0]),
        'job': {
            'job_id': t[2],
            'job_name': t[3],
            'job_desc': t[4]
        }
    }

class WorkerHelper:
    @staticmethod
    @format_by_formater(worker_formatter)
    def get_by_id(worker_id):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select worker.id, worker.name, job.id, job.name, job.description'
            ' from worker, job where worker.id=%s and worker.job_id = job.id', 
            [worker_id]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(worker_formatter)
    def get_by_name(worker_name):
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select worker.id, worker.name, job.id, job.name, job.description'
            ' from worker, job where worker.id=%s and worker.job_id = job.id', 
            [worker_name]
            )
        return cursor.fetchone()

    @staticmethod
    @format_by_formater(worker_formatter, True)
    def get_all():
        cursor = mysql.get_db().cursor()
        cursor.execute(
            'select worker.id, worker.name, job.id, job.name, job.description'
            ' from worker, job where worker.job_id = job.id'
            )
        return cursor.fetchall()

    @staticmethod
    def filter_by_department(item_list, depart_id):
        def in_depart(worker):
            for depart in worker['departments']:
                if depart['depart_id'] == depart_id:
                    return True
            return False

        return filter(in_depart, item_list)

    @staticmethod
    def create_worker(worker_name, worker_job_id, worker_depart_ids):
        if WorkerHelper.get_by_name(worker_name) is not None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "insert into worker (name, job_id) "
            "values (%s, %s)", 
            (worker_name, worker_job_id)
            )
        db.commit()
        if cursor.rowcount != 1:
            return False
        
        worker = WorkerHelper.get_by_name(worker_name)
        if not worker:
            return False
        success = True
        for depart_id in worker_depart_ids:
            if not WorkerHelper.add_worker_depart(worker['worker_id'], depart_id):
                success = False

        if success:
            return True
        else:
            abort(400)
            return False

    @staticmethod
    def modify(worker_id, fields):
        if WorkerHelper.get_by_id(worker_id) is None:
            return False

        set_sql = reduce(
            (lambda s1, s2: s1 +',' + s2), 
            ["{}=%s".format(k) for (k, v) in fields]
            )
        print set_sql

        arg_list = [v for (k, v) in fields]
        arg_list.append(worker_id)
        print arg_list
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "update worker set {} where id=%s".format(set_sql),
            arg_list
            )
        db.commit()
        return cursor.rowcount == 1

    @staticmethod
    def delete_by_id(worker_id):
        if WorkerHelper.get_by_id(worker_id) is None:
            return False
            
        db = mysql.get_db()
        cursor = db.cursor()
        cursor.execute(
            "delete from worker where id=%s", 
            (worker_id,)
            )
        db.commit()
        return cursor.rowcount == 1

