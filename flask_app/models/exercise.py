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
    def validate_sighting(form):
        is_valid = True
        if int(form['number']) < 1:
            flash("You can't report a sighting with no sasquatches! You were just outside!")
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
    def get_one_sighting(cls, sightingid):
        data={
            'id': sightingid
        }
        query = "SELECT * FROM sightings where id = %(id)s;"
        results = connectToMySQL('sasquatch').query_db(query,data)
        return cls(results[0])


    @classmethod
    def delete_exercise(cls, sightingid):
        data = {
            'id' : sightingid
        }
        query="""DELETE FROM sightings WHERE id = %(id)s"""
        return connectToMySQL('sasquatch').query_db( query, data )

    @classmethod
    def create_sighting(cls,form):
        data={
            'location': form['location'],
            'what_happened':form['what_happened'],
            'date':form['date'],
            'number':form['number'],
            'users_id' : session['id'],
        }
        query = """INSERT INTO sightings (location, what_happened, date, number,users_id) 
        VALUES (%(location)s, %(what_happened)s, %(date)s, %(number)s,%(users_id)s);"""
        return connectToMySQL('sasquatch').query_db( query, data )
    
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




