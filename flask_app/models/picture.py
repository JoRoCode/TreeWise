from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import tree

class Picture:
    db = "treewise"
    def __init__(self, data):
        self.id = data['id']
        self.path = data['path']
        self.attribute = data['attribute']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tree = None
        
        
    # Create Picture method
    @classmethod
    def add_picture_to_database(cls, path, attribute,tree_id):
        picture_data = {'path': path,
                        'attribute' : attribute,
                        'tree_id': tree_id}
        query = """
            INSERT INTO
                pictures
                    (path,
                    attribute,
                    tree_id)
            VALUES
                (%(path)s,
                %(attribute)s,
                %(tree_id)s);
            """
        results = connectToMySQL(cls.db).query_db(query,picture_data)
        return results
    
    # Read Picture Method

    @classmethod
    def get_pictures_by_tree_common_name(cls,data):
        common_name = {'common_name': data}
        query = """
            SELECT *
            FROM pictures
            LEFT JOIN trees 
            ON trees.id = pictures.tree_id
            WHERE common_name = %(common_name)s;
            """
        results = connectToMySQL(cls.db).query_db(query, common_name)
        all_pictures = []
        for result in results:
            this_picture = cls(result)
            this_picture.tree = tree.Tree.instantiate_tree(result)
            all_pictures.append(this_picture)
        return all_pictures