from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User


@app.route('/user/register', methods={'POST'})
def register():
    is_valid, errors = User.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        return render_template("login.html")

    if request.form["password"] != request.form.get("password_confirmation"):
        flash("Password and password confirmation must be equal!", "error")
        return render_template("login.html")

    User.save({
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': User.hash_password(request.form['password']),
    })
    user = User.get_user_by_email(request.form["email"])
    flash('Thank you for registering')

    session["uid"] = user.id
    return redirect("/login")