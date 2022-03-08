from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user
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
        self.difficulty = []
        self.likes=[]
        self.comments=[]
    # ************MUST EDIT DIFFICULTY AFTER SUCCESFUL CREATION*******************************************

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
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL('sasquatch').query_db(query)
        sightings = []
        if not len(results)<1:
            for sighting in results:
                sightings.append( cls(sighting)) 
        return sightings
        
    @classmethod
    def get_one_exercise(cls, sightingid):
        data={
            'id': sightingid
        }
        query = "SELECT * FROM exercises where id = %(id)s;"
        results = connectToMySQL('exercise').query_db(query,data)
        return cls(results[0])


    @classmethod
    def delete_exercise(cls, sightingid):
        data = {
            'id' : sightingid
        }
        query="""DELETE FROM sightings WHERE id = %(id)s"""
        return connectToMySQL('sasquatch').query_db( query, data )

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
    def update_sighting(cls,form):
        data={
            'id' : form['id'],
            'location': form['location'],
            'what_happened':form['what_happened'],
            'date':form['date'],
            'number':form['number'],
            'users_id':session['id']
        }
        query = """UPDATE sightings
        SET location = %(location)s, what_happened = %(what_happened)s, date = %(date)s, number = %(number)s, updated_at = NOW()
        WHERE id=%(id)s;"""
        return connectToMySQL('sasquatch').query_db( query, data )

    @classmethod
    def get_this_sighting(cls,data):
        query = "SELECT * FROM sightings WHERE id = %(id)s"
        return connectToMySQL('sasquatch').query_db(query,data)




