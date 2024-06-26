
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db = "treewise" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.occupation = data['occupation']
        self.company_name = data['company_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.confirm_password = None
        self.comments = []




    # Create Users Models
    @classmethod
    def create_new_user(cls,user_data):
        if not cls.validate_user_on_register(user_data): return False
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        query = """
            INSERT INTO 
                users 
                    (first_name, 
                    last_name, 
                    email, 
                    company_name, 
                    occupation, 
                    password)
            VALUES (
                %(first_name)s, 
                %(last_name)s, 
                %(email)s, 
                %(company_name)s, 
                %(occupation)s, 
                %(password)s);
            """
        user_id = connectToMySQL(cls.db).query_db(query,user_data)
        session['user_id'] = user_id
        session['first_name'] = user_data['first_name']
        return user_id


    # Read Users Models
    @classmethod
    def get_user_by_id(cls,data):
        id = {'id': data}
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,id)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def get_user_by_email(cls,data):
        email= {'email' : data}
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s;
            """
        result = connectToMySQL(cls.db).query_db(query,email)
        if result:
            return cls(result[0])
        return False

    # Update Users Models

    @classmethod
    def update_user_info(cls,data):
        if not cls.validate_user_on_update(data): return False
        query = """
            UPDATE
                users
            SET
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                email = %(email)s,
                occupation = %(occupation)s,
                company_name = %(company_name)s
            WHERE
                id = %(id)s;"""
        connectToMySQL(cls.db).query_db(query,data)
        return True

    # Delete Users Models
    
    @classmethod
    def delete_user_account(cls,data):
        id = {'id' : data}
        
        query = """
            DELETE FROM
            comments
            WHERE comments.user_id = %(id)s;
            """
        connectToMySQL(cls.db).query_db(query,id)
        query2 = """
            DELETE FROM
            quizs
            WHERE quizs.user_id = %(id)s;
            """
        connectToMySQL(cls.db).query_db(query2,id)
        query3 = """
            DELETE FROM
            users
            WHERE id = %(id)s;
            """
        return connectToMySQL(cls.db).query_db(query3,id)
        
    
    # login
    
    @classmethod
    def log_user_in(cls,data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['first_name'] = this_user.first_name
                return True
        flash('Invalid email or password')
        return False
    
# instantiate user

    @classmethod
    def instantiate_user(cls, data):
        if 'users.id' in data:
            return cls({
                'id' : data['users.id'],
                'first_name' : data['first_name'],
                'last_name' : data['last_name'],
                'email' : data['email'],
                'company_name' : data['company_name'],
                'occupation' : data['occupation'],
                'password' : data['password'],
                'created_at' : data['users.created_at'],
                'updated_at' : data['users.updated_at']})
        return cls(data)


    # validations
    
    @classmethod
    def validate_user_on_register(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First name is required")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required")
            is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 charicters.")
            is_valid = False
        if len(data['confirm_password']) < 1:
            flash("Confirm Password is required.")
            is_valid = False
        if not data["password"] == data["confirm_password"]:
            flash("Your password must match confirm password.")
            is_valid = False
        if cls.get_user_by_email(data['email']):
            flash('There is already an account with that email')
            is_valid = False
        return is_valid
            

    @classmethod
    def validate_user_on_update(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 1:
            flash("First name is required")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name is required")
            is_valid = False
        if len(data['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid