
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tree:
    db = "treewise" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.common_name = data['common_name']
        self.scientific_name = data['scientific_name']
        self.tree_order = data['tree_order']
        self.family = data['family']
        self.genus = data['genus']
        self.species = data['species']
        self.deciduous = data['deciduous']
        self.mature_height = data['mature_height']
        self.mature_diameter = data['mature_diameter']
        self.growth_rate = data['growth_rate']
        self.hardiness_zone = data['hardiness_zone']
        self.leaf_type = data['leaf_type']
        self.spring_foliage = data['spring_foliage']
        self.fall_foliage = data['fall_foliage']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pictures = []


    # Create Tree Models
    @classmethod
    def create_new_tree(cls,tree_data):
        if not cls.validate_tree(tree_data): return False
        print(tree_data)
        query = """
            INSERT INTO
                trees
                (common_name,
                scientific_name,
                tree_order,
                family,
                genus,
                species,
                deciduous,
                mature_height,
                mature_diameter,
                growth_rate,
                hardiness_zone,
                leaf_type,
                spring_foliage,
                fall_foliage,
                description)
            VALUES
                (%(common_name)s,
                %(scientific_name)s,
                %(tree_order)s,
                %(family)s,
                %(genus)s,
                %(species)s,
                %(deciduous)s,
                %(mature_height)s,
                %(mature_diameter)s,
                %(growth_rate)s,
                %(hardiness_zone)s,
                %(leaf_type)s,
                %(spring_foliage)s,
                %(fall_foliage)s,
                %(description)s);
            """
        return connectToMySQL(cls.db).query_db(query,tree_data)
        
    
    
    # Read Users Models
    @classmethod
    def get_tree_by_id(cls,data):
        query = """
            SELECT *
            FROM trees
            WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_tree_by_common_name(cls,data):
        common_name = {'common_name' : data}
        query = """
            SELECT *
            FROM trees
            WHERE common_name = %(common_name)s;"""
        results = connectToMySQL(cls.db).query_db(query,common_name)
        if results:
            return cls(results[0])
        return False


    @classmethod
    def get_tree_by_multiple_varieables(cls,data):
        tree_name = {'common_name': data,
                    'scientific_name' : data}
        query = """
            SELECT common_name
            FROM trees
            WHERE common_name = %(common_name)s
            OR scientific_name = %(scientific_name)s;"""
        results = connectToMySQL(cls.db).query_db(query,tree_name)
        if results:
            return results[0]['common_name']
        return False
    
    
    @classmethod
    def get_tree_by_common_name_with_pictures(cls,data):
        common_name = {'common_name' : data}
        query = """
            SELECT *
            FROM trees
            LEFT JOIN pictures
            ON trees.id = pictures.tree_id
            WHERE common_name = %(common_name)s;
            """
        result = connectToMySQL(cls.db).query_db(query,common_name)
        print(result, "RESULT!!!!!!!!!!!!")
        this_tree = cls(result[0])
        this_tree.pictures.append({
            'pictures.id': 'pictures.id',
            'path' : 'path',
            'attribute' : 'attribute',
            'created_at' : 'pictures.created_at',
            'updated_at' : 'pictures.updated_at',
            'tree_id' : this_tree.id})
        if result:
            return this_tree
        return False

    @classmethod
    def get_all_trees(cls):
        query = """
            SELECT *
            FROM trees;
            """
        results = connectToMySQL(cls.db).query_db(query)
        all_trees = []
        for result in results:
            this_tree = cls(result)
            all_trees.append(this_tree)
        return all_trees
    
    @classmethod
    def get_all_trees_with_pictures(cls):
        query = """
            SELECT *
            FROM trees
            LEFT JOIN pictures
            ON trees.id = pictures.tree_id;
            """
        results = connectToMySQL(cls.db).query_db(query)
        all_trees = []
        for result in results:
            this_tree = cls(result)
            this_tree.pictures.append({
            'pictures.id': 'pictures.id',
            'path' : 'path',
            'attribute' : 'attribute',
            'created_at' : 'pictures.created_at',
            'updated_at' : 'pictures.updated_at',
            'tree_id' : this_tree.id})
            all_trees.append(this_tree)
        return all_trees
    

    # Update trees Models
    @classmethod
    def update_this_tree(cls,data):
        if not cls.validate_tree(data): return False
        query = """
            UPDATE
                trees
            SET
                common_name = %(common_name)s,
                scientific_name = %(scientific_name)s,
                tree_order = %(tree_order)s,
                family = %(family)s,
                genus = %(genus)s,
                species = %(species)s,
                deciduous = %(deciduous)s,
                mature_height = %(mature_height)s,
                mature_diameter = %(mature_diameter)s,
                growth_rate = %(growth_rate)s,
                hardiness_zone = %(hardiness_zone)s,
                leaf_type = %(leaf_type)s,
                spring_foliage = %(spring_foliage)s,
                fall_foliage = %(fall_foliage)s,
                description = %(description)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query,data)
        return True


    # Delete Trees Models
    
    @classmethod
    def delete_tree(cls,id):
        query = """
            DELETE FROM
            trees
            WHERE id = %(id)s;
            """
        connectToMySQL(cls.db).query_db(query,id)
        return
    
    # Instantiate tree

    @classmethod
    def instantiate_tree(cls, data):
        if 'tree.id' in data:
            return cls({
                "id" : data['id'],
                "common_name" : data['common_name'],
                "scientific_name" : data['scientific_name'],
                "order" : data['order'],
                "family" : data['family'],
                "gunus" : data['gunus'],
                "species" : data['species'],
                "decicuous" : data['decicuous'],
                "mature_height" : data['mature_height'],
                "mature_diameter" : data['mature_diameter'],
                "growth_rate" : data['growth_rate'],
                "hardiness_zone" : data['hardiness_zone'],
                "leaf_type" : data['leaf_type'],
                "spring_foliage" : data['spring_foliage'],
                "fall_foliage" : data['fall_foliage'],
                "description" : data['description'],
                "created_at" : data['created_at'],
                "updated_at" : data['updated_at']})
        return cls(data)

    @classmethod
    def validate_tree(cls,data):
        is_valid = True
        if len(data['common_name']) < 1:
            flash("Common name is required")
            is_valid = False
        if len(data['scientific_name']) < 1:
            flash("Scientific name is required")
            is_valid = False
        if len(data['tree_order']) < 1:
            flash("Order is required")
            is_valid = False
        if len(data['family']) < 1:
            flash("Family is required")
            is_valid = False
        if len(data['genus']) < 1:
            flash("Genus is required")
            is_valid = False
        if len(data['species']) < 1:
            flash("Species is required")
            is_valid = False
        if len(data['deciduous']) < 1:
            flash("Deciduous or Evergreen is required")
            is_valid = False
        if len(data['mature_height']) < 1:
            flash("Mature Height is required")
            is_valid = False
        if len(data['mature_diameter']) < 1:
            flash("Mature Diameter is required")
            is_valid = False
        if len(data['growth_rate']) < 1:
            flash("Growth Rate is required")
            is_valid = False
        if len(data['hardiness_zone']) < 1:
            flash("Hardiness Zone is required")
            is_valid = False
        if len(data['leaf_type']) < 1:
            flash("Leaf Type is required")
            is_valid = False
        if len(data['spring_foliage']) < 1:
            flash("Spring Foliage is required")
            is_valid = False
        if len(data['fall_foliage']) < 1:
            flash("Fall Foliage is required")
            is_valid = False
        if len(data['description']) < 1:
            flash("Description is required")
            is_valid = False
        return is_valid