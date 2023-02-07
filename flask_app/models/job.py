from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Job:
    db_name='project'
    def __init__(self,data):
        self.id=data['id'],
        self.title=data['title'],
        self.description=data['description'],
        self.location=data['location'],
        self.created_at=data['created_at'],
        self.update_at=data['update_at']

    @classmethod
    def get_all_jobs(cls):
        query='SELECT * FROM jobs;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        jobs= []
        for row in results:
            jobs.append(row)
        return jobs

    @classmethod
    def get_job_by_id(cls,data):
        query='SELECT * FROM jobs WHERE id=%(job_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return results[0]

    @classmethod
    def get_user_job(cls,data):
        query='SELECT * FROM jobs LEFT JOIN users ON jobs.user_id= users.id LEFT JOIN myjob on myjob.job_id = jobs.id and myjob.user_id = users.id WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        jobs= []
        if results:
            for row in results:
                jobs.append(row)
            return jobs
        return jobs

    @classmethod
    def get_user_added_job(cls,data):
        query='SELECT * FROM myjob LEFT JOIN jobs on myjob.job_id = jobs.id WHERE myjob.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        jobs= []
        if results:
            for row in results:
                jobs.append(row)
            return jobs
        return jobs
    
    
    @classmethod
    def get_user_added_jobIds(cls,data):
        query='SELECT myjob.job_id FROM myjob WHERE myjob.user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        jobs= []
        if results:
            for row in results:
                jobs.append(row)
            return jobs
        return jobs
        
    @classmethod
    def create_job(cls,data):
        query='INSERT INTO jobs (title,description,location,user_id) VALUES (%(title)s, %(description)s,%(location)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_job(cls,data):
        query = 'UPDATE jobs SET title=%(title)s, description =%(description)s,location =%(location)s, user_id = %(user_id)s WHERE jobs.id = %(job_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM jobs WHERE id=%(job_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def addMyJob(cls,data):
        query= 'INSERT INTO myjob (job_id, user_id) VALUES (%(job_id)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_job(job):
        is_valid=True
        if len(job['title']) < 3:
            flash("Title is required", 'title')
            is_valid = False
        if len(job['description']) < 3:
            flash("Description is required", 'description')
            is_valid = False
        if len(job['location']) < 3:
            flash("Location is required", 'location')
            is_valid = False
        return is_valid