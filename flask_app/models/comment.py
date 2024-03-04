
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, request
from flask_app.models import user


class Comment:
    db = "treewise" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None




    # Create Comment Models
    @classmethod
    def create_new_comment(cls, comment_data):
        if not cls.validate_comment_on_submit(comment_data): return False
        query = """
            INSERT INTO 
                comments 
                (comment, 
                user_id)
            VALUES (
                %(comment)s,
                %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query,comment_data)



    # Read Comment Models
    @classmethod
    def get_comment_by_id(cls,id):
        data = {'id': id}
        query = """
            SELECT *
            FROM comments
            WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all_comments_with_creator(cls):
        query = """
            SELECT *  
            FROM comments
            LEFT JOIN users 
            ON users.id = comments.user_id
            ORDER BY comments.id DESC;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_comments = []
        for result in results:
            this_comment = cls(result)
            this_comment.creator = user.User.instantiate_user(result)
            all_comments.append(this_comment)
        return all_comments
    
    @classmethod
    def get_one_comment_by_id_with_creator(cls,id):
        data = {'id': id}
        query = """
            SELECT *
            FROM comments
            LEFT JOIN users
            ON users.id = comments.user_id
            WHERE comments.id = %(id)s
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        for result in results:
            this_comment = cls(result)
            this_comment.creator = user.User.instantiate_user(results[0])
        return this_comment
    
    # Update Comments Models
    
    @classmethod
    def update_user_comment(cls,data):
        if not cls.validate_comment_on_submit(data): return False
        query = """
            UPDATE
            comments
            SET
            comment = %(comment)s
            WHERE
            id = %(id)s;
        """
        connectToMySQL(cls.db).query_db(query,data)
        return True


    # Delete Comments Models
    
    @classmethod
    def delete_user_comment(cls,id):
        data = {'id': id}
        query = """
            DELETE FROM
            comments
            WHERE id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

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
    def validate_comment_on_submit(cls, data):
        is_valid = True
        if len(data['comment']) < 1:
            flash("You cannot submit a blank comment.")
            is_valid = False
        return is_valid
