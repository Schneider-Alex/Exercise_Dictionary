from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_app.models import exercise, user

class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.written_by = data['written_by']
        self.written_for = data['written_for']

    @staticmethod
    def validate_comment( form ):
        is_valid = True
        if len(form['content'])<3:
            flash("Comment must be atleast 3 characters")
            is_valid = False
        return is_valid

    @classmethod
    def create_comment(cls,form):
        data={
            'content': form['content'],
            'exercise_id':form['exercise_id'],
            'user_id': session['id'],
        }
        query = """INSERT INTO comments (content, exercise_id, user_id) 
        VALUES (%(content)s, %(exercise_id)s, %(user_id)s);"""
        return connectToMySQL('exercise').query_db( query, data )


    @classmethod
    def get_one_comments_author(cls,commentid):
        data={
            'id': commentid
        }
        query = """SELECT * FROM comments
        JOIN users ON comments.user_id = users.id 
        JOIN exercises ON comments.exercise_id = exercises.id
        where comments.id = %(id)s;"""
        row_from_db = connectToMySQL('exercise').query_db(query,data)
        print(row_from_db[0])
        comment_data ={
                    "content" : row_from_db[0]["content"],
                    "id" : row_from_db[0]["id"],
                    "written_by" : row_from_db[0]["first_name"] + " " + row_from_db[0]["last_name"],
                    "written_for" : row_from_db[0]["name"]
                }
        return cls(comment_data)

