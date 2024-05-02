from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def list_recipes():

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    user = User.get_user_by_id(session["uid"])
    return render_template(
        "recipes.html",
        current_user=user,
        recipes=Recipe.get_all()
    )


@app.route('/recipes/<recipe_id>')
def view_recipe(recipe_id):

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    user = User.get_user_by_id(session["uid"])
    return render_template(
        "viewrecipe.html",
        current_user=user,
        recipe=Recipe.get_recipe_by_id(recipe_id)
    )


@app.route('/recipes/<recipe_id>/edit')
def edit_recipe_page(recipe_id):

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    user = User.get_user_by_id(session["uid"])
    return render_template(
        "editrecipe.html",
        current_user=user,
        recipe=Recipe.get_recipe_by_id(recipe_id)
    )

@app.route('/recipes/<recipe_id>/edit', methods=['POST'])
def edit_recipe(recipe_id):
    
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    recipe = Recipe.get_recipe_by_id(recipe_id)
    if int(recipe.user_id) != session["uid"]:
        flash("You don't have permissions to edit this recipe!")
        return redirect("/recipes/" + recipe_id + "/edit")

    user = User.get_user_by_id(session["uid"])

    is_valid, errors = Recipe.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
    else:
        Recipe.edit_recipe({
            "id": recipe_id,
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "under": request.form["under"],
            "made_at": request.form["made_at"],
        })

    return render_template(
        "editrecipe.html",
        current_user=user,
        recipe=Recipe.get_recipe_by_id(recipe_id)
    )


@app.route('/recipes/<recipe_id>/delete')
def delete_recipe(recipe_id):
    
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    recipe = Recipe.get_recipe_by_id(recipe_id)
    if int(recipe.user_id) != session["uid"]:
        flash("You don't have permissions to delete this recipe!")
    else:
        Recipe.delete_recipe_by_id(recipe_id)
        flash("Successfully deleted recipe!")

    return redirect("/recipes")


@app.route('/recipes/new')
def new_recipe_page():
    
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    user = User.get_user_by_id(session["uid"])
    return render_template(
        "createrecipe.html",
        current_user=user,
    )


@app.route('/recipes/new', methods=['POST'])
def add_new_recipe():
    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")

    is_valid, errors = Recipe.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        return redirect("/recipes/new")

    Recipe.save({
        "user_id": session["uid"],
        "name": request.form["name"],
        "under": int(request.form["under"]),
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "made_at": request.form["made_at"]
    })
    return redirect("/recipes")
