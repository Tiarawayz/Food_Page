from flask_app.config.mysqlconnection import connectToMySQL


class Recipe:
  DB = 'user_recipe'

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.made_at = data['made_at']
    self.name = data['name']
    self.under = data['under']
    self.posted_by = data.get('posted_by')
    self.instructions = data['instructions']
    self.description = data['description']

  @classmethod
  def save (cls, data):
    query = """INSERT into recipes (name, under, instructions, description, user_id, made_at, created_at, updated_at) 
VALUES (%(name)s, %(under)s, %(instructions)s, %(description)s, %(user_id)s, %(made_at)s, NOW(),NOW());"""
    results = connectToMySQL('user_recipe').query_db(query, data)
    return results

  @classmethod
  def get_recipe_by_id(cls, id):
    query = """SELECT recipes.id as id, name, under, instructions, description, made_at, recipes.created_at, recipes.updated_at, user_id, first_name AS posted_by FROM
    recipes JOIN user ON user.id = recipes.user_id WHERE recipes.id = %(id)s;"""
    results = connectToMySQL('user_recipe').query_db(query, {"id": id})
    return cls(results[0])

  @classmethod
  def get_all(cls):
    query = """SELECT recipes.id as id, name, under, instructions, description, made_at, recipes.created_at, recipes.updated_at, user_id, first_name AS posted_by FROM
    recipes JOIN user ON user.id = recipes.user_id;"""
    results = connectToMySQL('user_recipe').query_db(query)
    if not results:
      return []
    return [cls(row) for row in results]

  @classmethod
  def edit_recipe(cls, data):
    query = """UPDATE recipes SET name=%(name)s, under=%(under)s, instructions=%(instructions)s,
    description=%(description)s, made_at=%(made_at)s WHERE recipes.id = %(id)s;"""
    results = connectToMySQL('user_recipe').query_db(query, data)
    return results

  @classmethod
  def delete_recipe_by_id(cls, id):
    query = """DELETE FROM recipes WHERE id = %(id)s;"""
    results = connectToMySQL('user_recipe').query_db(query, {"id": id})
    return results

  @staticmethod
  def validate(data):
      errors = []

      required_fields = ('name', 'under', 'description', 'instructions', 'made_at')
      for required_field in required_fields:
        if required_field not in data:
          errors.append(f"Missing required field '{required_field}'!")


      if len(data["name"]) < 2:
        errors.append("Name must contain atleast 2 characters.")

      if len(data["instructions"]) < 3:
        errors.append("Instructions must contain atleast 8 characters.")

      if len(data["description"]) < 3:
        errors.append("Description must contain atleast 8 characters.")

      is_valid = len(errors) == 0
      return is_valid, errors
