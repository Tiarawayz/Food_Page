from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_session import Session
from flask_app.models.user import User


Session(app)


@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/login', methods=['POST'])
def login_post():

    user = User.get_user_by_email(request.form["email"])
    if user is None or not User.verify_password(user, request.form["password"]):
        flash("Incorrect email or password!", "warning")
        return render_template("login.html")


    session["uid"] = user.id
    return redirect("/recipes")


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("uid")
    return redirect("/login")
