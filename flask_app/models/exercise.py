from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user, comment
bcrypt = Bcrypt(app)

class Exercise:
    def __init__( self , data ):
        self.id = data['id']
        self.name=data['name']
        self.description = data['description']
        self.primary_muscle = data['primary_muscle']
        self.secondary_muscle = data['secondary_muscle']
        self.equipment = data ['equipment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.main_group_id=data['main_group_id']
        self.user_id  = data['user_id']
        self.created_by= user.User.get_one_users_name(self.user_id)
        self.likes=[]
        self.comments=[]

    @staticmethod
    def validate_exercise(form):
        is_valid = True
        if len(form['name']) < 2:
            flash("Exercise name must be greater than 2 characters")
            is_valid = False
        if len(form['description']) < 25:
            flash("Description must be atleast 25 characters")
            is_valid = False
        if len(form['primary_muscle']) < 3:
            flash("Primary Muscle name must be atleast 3 characters")
            is_valid = False
        if len(form['secondary_muscle']) < 3:
            flash("Secondary Muscle name must be atleast 3 characters")
            is_valid = False
        if len(form['equipment']) < 3:
            flash("Equipment must be atleast 3 characters")
            is_valid = False
        return is_valid
        
    @classmethod
    def get_one_exercise(cls, exerciseid):
        data={
            'id': exerciseid
        }
        query = """SELECT * FROM exercises 
        where id = %(id)s;"""
        results = connectToMySQL('exercise').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one_exercises_comments(cls, exerciseid):
        data={
            'id': exerciseid
        }
        query = """SELECT * FROM exercises
        LEFT JOIN comments ON exercises.id=comments.exercise_id
        LEFT JOIN users ON users.id=comments.user_id
        WHERE exercises.id= %(id)s"""
        results = connectToMySQL('exercise').query_db(query,data)
        Exercise=cls(results[0])
        if results[0]["content"]:
            for row_from_db in results:
                comment_data ={
                    "content" : row_from_db["content"],
                    "id" : row_from_db["comments.id"],
                    "written_by" : row_from_db["first_name"] + " " + row_from_db["last_name"],
                    "written_for" : row_from_db["name"]
                }
                Exercise.comments.append(comment.Comment(comment_data))
        return Exercise

    @classmethod
    def count_one_exercises_likes(cls, exerciseid):
        data={
            'id': exerciseid
        }
        query = """SELECT COUNT(*) FROM likes 
        where exercise_id = %(id)s;"""
        results = connectToMySQL('exercise').query_db(query,data)
        if not results:
            return 0
        return results
    
    @classmethod
    def get_one_exercises_likes(cls, exerciseid):
        data={
            'exercise_id': exerciseid,
            'user_id' : session['id']
        }
        query = """SELECT * FROM likes 
        where user_id = %(user_id)s and exercise_id =%(exercise_id)s;"""
        results = connectToMySQL('exercise').query_db(query,data)
        return results

    @classmethod
    def delete_exercise_and_comments_and_likes(cls, exerciseid):
        data = {
            'id' : exerciseid
        }
        query="""DELETE FROM likes WHERE exercise_id = %(id)s"""
        connectToMySQL('exercise').query_db( query, data )
        query="""DELETE FROM comments WHERE exercise_id = %(id)s"""
        connectToMySQL('exercise').query_db( query, data )
        query="""DELETE FROM exercises WHERE id = %(id)s"""
        return connectToMySQL('exercise').query_db( query, data )

    @classmethod
    def create_exercise(cls,form):
        
        data={
            'name': form['name'],
            'description':form['description'],
            'primary_muscle':form['primary_muscle'],
            'secondary_muscle':form['secondary_muscle'],
            'equipment' : form['equipment'],
            'main_group' : form['main_group'],
            'user_id' : session['id'],
        }
        query = """INSERT INTO exercises (name, description, primary_muscle, secondary_muscle,equipment,main_group_id,user_id) 
        VALUES (%(name)s, %(description)s, %(primary_muscle)s, %(secondary_muscle)s,%(equipment)s,%(main_group)s,%(user_id)s);"""
        return connectToMySQL('exercise').query_db( query, data )

    @classmethod
    def like_exercise(cls,exerciseid):
        data={
            'user_id' : session['id'],
            'exercise_id' : exerciseid
        }
        query = """INSERT INTO likes (user_id, exercise_id) 
        VALUES (%(user_id)s,%(exercise_id)s);"""
        return connectToMySQL('exercise').query_db( query, data )

    @classmethod
    def unlike_exercise(cls,exerciseid):
        data={
            'user_id' : session['id'],
            'exercise_id' : exerciseid
        }
        query = """DELETE FROM likes 
        WHERE user_id = %(user_id)s and  exercise_id = %(exercise_id)s;"""
        return connectToMySQL('exercise').query_db( query, data )

    @classmethod
    def update_exercise(cls,form):
        data={
            'id' : form['id'],
            'name': form['name'],
            'description':form['description'],
            'primary_muscle':form['primary_muscle'],
            'secondary_muscle':form['secondary_muscle'],
            'equipment':form['equipment']
        }
        query = """UPDATE exercises
        SET name = %(name)s, equipment = %(equipment)s, description = %(description)s, primary_muscle = %(primary_muscle)s, primary_muscle = %(secondary_muscle)s, updated_at = NOW()
        WHERE id=%(id)s;"""
        return connectToMySQL('exercise').query_db( query, data )





