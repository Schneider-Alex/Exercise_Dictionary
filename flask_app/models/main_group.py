from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_app.models import exercise, user

class Group:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.exercises = []

    @classmethod
    def get_all_main_groups(cls):
        query = "SELECT * FROM main_groups;"
        results = connectToMySQL('exercise').query_db(query)
        main_groups = []
        if not len(results)<1:
            for group in results:
                main_groups.append( cls(group)) 
        return main_groups
    
    # @classmethod
    # def get_one_main(cls):
    #     data = {
    #         'id' : main_id
    #     } 
    #     query = "SELECT * FROM main_groups WHERE id = %(id)s;"
    #     results = connectToMySQL('exercise').query_db(query,data)
    #     main_groups = []
    #     if not len(results)<1:
    #         for group in results:

    @classmethod
    def get_one_mains_exercises(cls,main_id):
        data = {
            'id' : main_id
        }
        query = """SELECT * FROM main_groups
        LEFT JOIN exercises ON main_groups.id = exercises.main_group_id 
        WHERE main_groups.id = %(id)s"""
        results = connectToMySQL('exercise').query_db(query,data)
        Group=[]
        if results:
            Group=cls(results[0])
            for row_from_db in results:
                exercise_data = {
                    "id" : row_from_db["exercises.id"],
                    "name" : row_from_db["exercises.name"],
                    "description" : row_from_db["description"],
                    "primary_muscle" : row_from_db["primary_muscle"],
                    "secondary_muscle" : row_from_db["secondary_muscle"],
                    "equipment" : row_from_db["equipment"],
                    "created_at" : row_from_db["created_at"],
                    "updated_at" : row_from_db["updated_at"],
                    "main_group_id" : row_from_db["main_group_id"],
                    "user_id" : row_from_db["user_id"]
                }
                Group.exercises.append(exercise.Exercise(exercise_data))
        return Group
