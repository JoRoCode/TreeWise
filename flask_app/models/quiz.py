from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

class Quiz:
    db = "treewise"
    def __init__(self, data):
        self.id = data['id']
        self.score = data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
# Create new quiz Model
    @classmethod
    def submit_quiz_results(cls, data):
        query = """
            INSERT INTO
                quizs
                (score,
                user_id)
            Values(
                %(score)s,
                %(user_id)s);
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result


# Read Quiz Methods

    @classmethod
    def get_all_quizs_by_user_id(cls,data):
        id = {'id': data}
        query = """
            SELECT *
            FROM quizs
            WHERE user_id = %(id)s;
        """
        results =  connectToMySQL(cls.db).query_db(query,id)
        if results:
            return results
        return False
        
        