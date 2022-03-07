from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import exercise

bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data ['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.sightings = []
    
    @staticmethod
    def validate_user( form ):
        is_valid = True
        query = """SELECT * FROM users WHERE email =  %(email)s"""
        results = connectToMySQL('exercise').query_db(query, form)
        if results:
            flash("email address already in use!")
            is_valid = False
        elif not EMAIL_REGEX.match(form['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(form['first_name']) < 2:
            flash("First Name must be 3 Characters!")
            is_valid = False
        if len(form['last_name']) <  2:
            flash("Last Name must be 3 Characters!")
            is_valid = False
        if form['passwordcheck'] != form['password']:
            flash('passwords do not match!')
            is_valid = False
        return is_valid

    @classmethod
    def get_one_users_name(cls, users_id):
        data = {
            'id' : users_id
        }
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL('exercise').query_db(query,data)
        full_name ='Someone'
        if results:
            user=cls(results[0])
            full_name = user.first_name + ' ' + user.last_name
        return full_name
    
    @classmethod
    def create_user(cls, form):
        data = {
                'first_name' : form['first_name'],
                'last_name' : form['last_name'],
                'email' : form['email'],
                'password' : bcrypt.generate_password_hash(form['password'])
            }
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL('exercise').query_db( query, data )
    
    @classmethod
    def login_user(cls, form):
        query = """SELECT * FROM users WHERE email =  %(email)s"""
        results = connectToMySQL('exercise').query_db(query, form)
        print(results)
        if len(results)<1:
            flash('Username or Password Incorrect')
            return False
        elif not bcrypt.check_password_hash(results[0]['password'], form['password'] ):
            flash('Username or Password Incorrect')
            return False
        logged_in_user=cls(results[0])
        session['id'] =logged_in_user.id
        session['first_name']=logged_in_user.first_name
        session['last_name'] = logged_in_user.last_name
        return True
